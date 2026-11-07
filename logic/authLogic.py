import hashlib
import hmac
import logging
import secrets
import smtplib
import socket
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import html

from config import (
    CODE_EXPIRY_MINUTES,
    MAX_ATTEMPTS,
    MAX_CODES_PER_HOUR,
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)
from extensions import db
from localization import CODE_MAIL_TEXTS, PASSKEY_MAIL_TEXTS
from templates.html_templates import HTML_CODE_TEMPLATE, HTML_PASSKEY_TEMPLATE

logger = logging.getLogger(__name__)


class LoginCode(db.Model):
    __tablename__ = "login_codes"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    code_hash = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def _send_mail(to_email: str, subject: str, text_body: str, html_body: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, [to_email], msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed — check SMTP_USER/SMTP_PASSWORD")
    except smtplib.SMTPRecipientsRefused:
        logger.warning("Email rejected for recipient: %s", to_email)
    except smtplib.SMTPException as e:
        logger.error("SMTP error sending to %s: %s", to_email, e)
    except (socket.timeout, ConnectionError, OSError) as e:
        logger.error("Connection error sending to %s: %s", to_email, e)
    return False


def send_code_email(to_email: str, code: str, language_code: str) -> bool:
    lang = language_code if language_code in CODE_MAIL_TEXTS else "en"
    t = CODE_MAIL_TEXTS[lang]
    m = CODE_EXPIRY_MINUTES

    html_body = HTML_CODE_TEMPLATE.format(
        lang=lang,
        intro=t["intro"],
        code=code,
        expiry=t["expiry"].format(m=m),
        sign=t["sign"],
        contact=t["contact"],
        privacy=t["privacy"],
    )
    text_body = t["text"].format(code=code, m=m)

    return _send_mail(to_email, t["subject"], text_body, html_body)


def _get_zone(tz_name: str | None) -> ZoneInfo:
    try:
        return ZoneInfo(tz_name or "UTC")
    except (ZoneInfoNotFoundError, ValueError):
        logger.warning("Unknown timezone %r, falling back to UTC", tz_name)
        return ZoneInfo("UTC")


def send_passkey_email(
    to_email: str,
    to_name:str,
    language_str: str,
    timezone_name: str = "UTC",
    created_at: datetime | None = None,
) -> bool:
    lang = language_str if language_str in PASSKEY_MAIL_TEXTS else "en"
    p = PASSKEY_MAIL_TEXTS[lang]

    created_at = created_at or datetime.now(timezone.utc)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    time_str = created_at.astimezone(_get_zone(timezone_name)).strftime("%H:%M")
    text = p["text"].format(m=time_str)
    intro = p["intro"].format(m=to_name)
    intro_html = p["intro"].format(m=html.escape(to_name or ""))

    html_body = HTML_PASSKEY_TEMPLATE.format(
        lang=lang,
        intro=intro_html,
        text=text,
        please_contact_1 = p["please_contact_1"],
        please_contact_2=p["please_contact_2"],
        please_contact_3=p["please_contact_3"],
        sign=p["sign"],
        contact=p["contact"],
        privacy=p["privacy"],
    )
    text_body = "\n\n".join([
        intro,
        p["text"].format(m=time_str),
        p["please_contact_1"]+" "+p["please_contact_2"]+" "+p["please_contact_3"],
        p["sign"].replace("<br>", "\n"),
    ])

    return _send_mail(to_email, p["subject"], text_body, html_body)


def too_many_codes(email: str) -> bool:
    since = datetime.utcnow() - timedelta(hours=1)
    count = LoginCode.query.filter(
        LoginCode.email == email,
        LoginCode.created_at >= since,
    ).count()
    return count >= MAX_CODES_PER_HOUR


def generate_and_send_code(email: str, language_code: str) -> None:
    # Invalidate any previous unused codes for this email
    LoginCode.query.filter_by(email=email, used=False).update({"used": True})

    code = f"{secrets.randbelow(1_000_000):06d}"

    login_code = LoginCode(
        email=email,
        code_hash=_hash_code(code),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=CODE_EXPIRY_MINUTES),
    )
    db.session.add(login_code)
    db.session.commit()

    send_code_email(email, code, language_code)


def verify_code(email: str, code: str) -> bool:
    entry = (
        LoginCode.query
        .filter_by(email=email, used=False)
        .order_by(LoginCode.created_at.desc())
        .first()
    )

    if not entry:
        return False

    if entry.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return False

    if entry.attempts >= MAX_ATTEMPTS:
        return False

    entry.attempts += 1

    if not hmac.compare_digest(entry.code_hash, _hash_code(code)):
        db.session.commit()
        return False

    entry.used = True
    db.session.commit()
    return True