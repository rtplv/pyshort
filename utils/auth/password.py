import bcrypt


def generate_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password, encoding="utf8"), salt).decode()


def validate_hash(password: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(bytes(password, encoding="utf8"), bytes(pwd_hash, encoding="utf8"))
