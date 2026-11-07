HTML_CODE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="dark" />
  <meta name="supported-color-schemes" content="dark" />
  <title>TichuStats</title>
</head>
<body style="margin:0; padding:0; background-color:#1c1c1e; color:#f5f5f7; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; -webkit-font-smoothing:antialiased;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#1c1c1e;">
    <tr>
      <td align="center" style="padding:80px 24px;">
        <table role="presentation" width="450" cellpadding="0" cellspacing="0" style="max-width:450px; width:100%; background-color:#1c1c1e; border:1px solid #2c2c2e; border-radius:18px; box-shadow:0 11px 34px rgba(0,0,0,0.65);">
          <tr>
            <td style="padding:65px 50px 55px; text-align:left;">
              <h1 style="margin:0 0 24px 0; font-size:34px; font-weight:600; letter-spacing:-0.374px; color:#f5f5f7; line-height:1.1;">TichuStats</h1>
              <p style="margin:0; font-size:17px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{intro}</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:20px; margin-bottom:20px;">
                <tr>
                  <td align="center" valign="middle" height="75" bgcolor="#252527" style="height:75px; padding:0; background-color:#252527; border:1px solid #2c2c2e; border-radius:12px; font-size:50px; line-height:75px; font-weight:700; letter-spacing:5px; color:#f5f5f7; text-align:center;">{code}</td>
                </tr>
              </table>
              <p style="margin:0; font-size:17px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{expiry}</p>
              <p style="margin:50px 0 0 0; font-size:14px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{sign}</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#1c1c1e;">
    <tr>
      <td align="center" style="border-top:1px solid #2c2c2e; padding:20px 24px; font-size:12px; letter-spacing:-0.12px; color:#a1a1a6;">
        <a href="mailto:leon@tichu.dev" style="color:#a1a1a6; text-decoration:none;">{contact}</a> | <a href="https://tichu.dev/privacy" style="color:#a1a1a6; text-decoration:none;">{privacy}</a>
      </td>
    </tr>
  </table>
</body>
</html>
"""

HTML_PASSKEY_TEMPLATE = """\
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="dark" />
  <meta name="supported-color-schemes" content="dark" />
  <title>TichuStats</title>
</head>
<body style="margin:0; padding:0; background-color:#1c1c1e; color:#f5f5f7; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; -webkit-font-smoothing:antialiased;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#1c1c1e;">
    <tr>
      <td align="center" style="padding:80px 24px;">
        <table role="presentation" width="450" cellpadding="0" cellspacing="0" style="max-width:450px; width:100%; background-color:#1c1c1e; border:1px solid #2c2c2e; border-radius:18px; box-shadow:0 11px 34px rgba(0,0,0,0.65);">
          <tr>
            <td style="padding:65px 50px 55px; text-align:left;">
              <h1 style="margin:0 0 24px 0; font-size:34px; font-weight:600; letter-spacing:-0.374px; color:#f5f5f7; line-height:1.1;">TichuStats</h1>
              <p style="margin:0; font-size:17px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{intro}</p>
              <p style="margin:20px 0 0 0; font-size:17px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{text}</p>
              <p style="margin:20px 0 0 0; font-size:17px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{please_contact_1} <a href="mailto:leon@tichu.dev" style="color:#f5f5f7; text-decoration:none;">{please_contact_2}</a> {please_contact_3}</p>
              <p style="margin:50px 0 0 0; font-size:14px; line-height:1.47; letter-spacing:-0.374px; color:#a1a1a6;">{sign}</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#1c1c1e;">
    <tr>
      <td align="center" style="border-top:1px solid #2c2c2e; padding:20px 24px; font-size:12px; letter-spacing:-0.12px; color:#a1a1a6;">
        <a href="mailto:leon@tichu.dev" style="color:#a1a1a6; text-decoration:none;">{contact}</a> | <a href="https://tichu.dev/privacy" style="color:#a1a1a6; text-decoration:none;">{privacy}</a>
      </td>
    </tr>
  </table>
</body>
</html>
"""