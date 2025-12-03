
from totp_utils import generate_totp_code, verify_totp_code

hex_seed = open("seed.txt").read().strip()

code = generate_totp_code(hex_seed)
print("Generated TOTP:", code)

print("Valid?", verify_totp_code(hex_seed, code))
