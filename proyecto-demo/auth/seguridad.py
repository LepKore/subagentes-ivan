import hashlib
import hmac
import secrets

ITERACIONES = 240000
LONGITUD_SALT = 16


def crear_hash(password, salt=None):
    """Devuelve (salt, hash) para una contraseña, sin almacenarla en claro."""
    if not isinstance(password, str):
        raise TypeError("password debe ser texto")
    salt = salt if salt is not None else secrets.token_bytes(LONGITUD_SALT)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERACIONES)
    return salt, digest


def verificar_password(password, salt, esperado):
    _, digest = crear_hash(password, salt)
    return hmac.compare_digest(digest, esperado)


def token_sesion():
    """Genera el secreto que se entrega al cliente (nunca se persiste en claro)."""
    return secrets.token_urlsafe(32)


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()
