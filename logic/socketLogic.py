from flask import session
from flask_jwt_extended import decode_token
from flask_socketio import join_room

from extensions import socketio

# Socket.IO rooms — every event goes only to the rooms that are allowed to see it:
#   user_<id>  one per logged-in app user (games, rounds, friend requests, settings)
#   players    all logged-in app users (profile list info: names, pictures, elo —
#              the same data /profilessimple already returns to every user)
#   dashboard  admin dashboard, sees everything
# A socket without a valid token stays connected (the login screen needs that)
# but is in no room, so it receives nothing.
PLAYERS = "players"
DASHBOARD = "dashboard"


def user_room(profile_id):
    return f"user_{profile_id}"


def _real_ids(profile_ids):
    # Guests have negative ids (or None) and no socket
    return {int(i) for i in profile_ids if i is not None and int(i) > 0}


def game_player_ids(game):
    return [game.team1_player1_id, game.team1_player2_id,
            game.team2_player1_id, game.team2_player2_id]


def emit_to_players(event, data):
    socketio.emit(event, data, to=[PLAYERS, DASHBOARD])


def emit_to_users(event, data, profile_ids):
    rooms = [user_room(i) for i in _real_ids(profile_ids)] + [DASHBOARD]
    socketio.emit(event, data, to=rooms)


def emit_to_game(event, data, game):
    emit_to_users(event, data, game_player_ids(game))


@socketio.on("connect")
def on_connect(auth=None):
    # Dashboard (browser, same origin): authenticated by the dashboard session cookie
    if session.get("jwt"):
        join_room(DASHBOARD)
        return

    token = auth.get("token") if isinstance(auth, dict) else None
    if not token:
        return  # anonymous: connected, but receives nothing

    try:
        payload = decode_token(token)
    except Exception:
        return

    from routes.auth_routes import is_token_revoked  # local import avoids a circular import
    if is_token_revoked(payload):
        return

    sub = str(payload.get("sub", ""))
    if not sub.isdigit():
        return
    join_room(user_room(int(sub)))
    join_room(PLAYERS)