import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key():
    """Load student's private RSA key"""
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def decrypt_seed_function(encrypted_seed_b64: str) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP (SHA-256)
    """
    private_key = load_private_key()

    # 1. Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. RSA OAEP decrypt
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. UTF-8
    seed_hex = decrypted_bytes.decode("utf-8")

    # 4. Validate
    if len(seed_hex) != 64:
        raise ValueError("Invalid seed length — expected 64 hex characters")

    return seed_hex
