import base64
import pyotp
import time  # <-- use Python's time module

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")

def generate_totp(hex_seed: str):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    
    # Calculate remaining time for current TOTP
    interval = 30
    current_time = int(time.time())
    valid_for = interval - (current_time % interval)
    
    return code, valid_for

def verify_totp(hex_seed: str, code: str):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=1)
