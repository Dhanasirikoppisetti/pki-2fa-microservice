

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
import subprocess

# Step 1: Get latest commit hash
commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%H']).decode().strip()
print("Commit Hash:", commit_hash)

# Step 2: Load your private key
with open('../student_private.pem', 'rb') as f:  # adjust path if needed
    private_key = load_pem_private_key(f.read(), password=None)

# Step 3: Sign commit hash with RSA-PSS
signature = private_key.sign(
    commit_hash.encode('utf-8'),  # Sign ASCII string
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Step 4: Load instructor public key
with open('../instructor_public.pem', 'rb') as f:  # adjust path if needed
    public_key = load_pem_public_key(f.read())

# Step 5: Encrypt the signature with RSA-OAEP
encrypted_signature = public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Step 6: Base64 encode
encoded = base64.b64encode(encrypted_signature).decode('utf-8')
print("Encrypted Commit Signature (Base64):", encoded)
