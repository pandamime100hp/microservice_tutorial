import datetime, jwt


def create(username: str, secret: str, is_admin: bool) -> str:
    current_time: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    expire: datetime.datetime = current_time + datetime.timedelta(days=1)

    payload: dict = {
        "username": username,
        "expire_at": str(expire),
        "issued_at": str(current_time),
        "is_admin": is_admin
    }

    return jwt.encode(
        payload=payload, 
        key=secret, 
        algorithm="HS256"
    )


def decode(token: str, secret: str) -> dict:
    return jwt.decode(
        jwt=token, 
        key=secret, 
        algorithms="HS256"
    )