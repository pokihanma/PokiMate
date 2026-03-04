from app.services.encryption_service import encrypt, decrypt, ciphertext_sha256


def test_encrypt_decrypt_roundtrip():
    plaintext = b"secret db content here"
    passphrase = "test-passphrase-123"
    salt, nonce, ciphertext = encrypt(plaintext, passphrase)
    assert len(salt) == 16
    assert len(nonce) == 12
    assert ciphertext != plaintext
    dec = decrypt(ciphertext, passphrase, salt, nonce)
    assert dec == plaintext


def test_ciphertext_sha256():
    data = b"hello"
    h = ciphertext_sha256(data)
    assert len(h) == 64
    assert h == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
