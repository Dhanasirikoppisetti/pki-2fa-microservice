
#!/usr/bin/env python3

import os
from datetime import datetime, timezone
import pyotp
import base64


def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")


def generate_totp_from_hex(hex_seed: str):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.now()


def main():
    seed_file = "/data/seed.txt"

    # 1. Read hex seed
    try:
        with open(seed_file, "r") as f:
            hex_seed = f.read().strip()
    except FileNotFoundError:
        print("Seed file not found.")
        return

    # 2. Generate TOTP code
    try:
        code = generate_totp_from_hex(hex_seed)
    except Exception as e:
        print(f"Error generating TOTP: {e}")
        return

    # 3. UTC timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # 4. Output
    print(f"{timestamp} - 2FA Code: {code}")


if __name__ == "__main__":
    main()
