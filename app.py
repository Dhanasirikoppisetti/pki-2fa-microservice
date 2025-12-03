from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import re
import time

from decrypt_seed import decrypt_seed_function
from totp_utils import generate_totp, verify_totp

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "2FA Microservice is running"}

# Your existing endpoints follow

DATA_DIR = "data"
SEED_FILE = os.path.join(DATA_DIR, "seed.txt")

os.makedirs(DATA_DIR, exist_ok=True)

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed_endpoint(request: DecryptRequest):
    try:
        seed = decrypt_seed_function(request.encrypted_seed)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

    if not re.fullmatch(r"[0-9a-fA-F]{64}", seed):
        raise HTTPException(status_code=500, detail={"error": "Decrypted seed is not a valid 64-character hex"})

    with open(SEED_FILE, "w") as f:
        f.write(seed)

    return {"status": "ok"}


@app.get("/generate-2fa")
def generate_2fa_endpoint():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    try:
        code = generate_totp(hex_seed)
        valid_for = 30 - (int(time.time()) % 30)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa_endpoint(request: VerifyRequest):
    if not request.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    try:
        is_valid = verify_totp(hex_seed, request.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

    return {"valid": is_valid}
