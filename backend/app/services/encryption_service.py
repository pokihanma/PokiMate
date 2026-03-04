"""
AES-256-GCM encryption for backup. Key derived via Argon2id (or scrypt fallback).
"""
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
try:
    from argon2.low_level import hash_secret_raw, Type
    HAS_ARGON2 = True
except ImportError:
    HAS_ARGON2 = False


def derive_key(passphrase: str, salt: bytes, kdf: str = "argon2id") -> bytes:
    if kdf == "argon2id" and HAS_ARGON2:
        return hash_secret_raw(
            secret=passphrase.encode(),
            salt=salt,
            time_cost=2,
            memory_cost=65536,
            parallelism=1,
            hash_len=32,
            type=Type.ID,
        )
    return Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(passphrase.encode())


def encrypt(plaintext: bytes, passphrase: str, salt: bytes | None = None, kdf: str = "argon2id") -> tuple[bytes, bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)
    key = derive_key(passphrase, salt, kdf)
    nonce = os.urandom(12)
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, plaintext, None)
    return salt, nonce, ciphertext


def decrypt(ciphertext: bytes, passphrase: str, salt: bytes, nonce: bytes, kdf: str = "argon2id") -> bytes:
    key = derive_key(passphrase, salt, kdf)
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None)


def ciphertext_sha256(ciphertext: bytes) -> str:
    return hashlib.sha256(ciphertext).hexdigest()
