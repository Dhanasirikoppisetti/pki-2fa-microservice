
import requests
import json

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"


def request_seed(student_id: str, github_repo_url: str):
    # 1. Read your student public key (PEM)
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    # 2. Build request JSON payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # 3. Send POST request
    response = requests.post(
        API_URL,
        json=payload,
        timeout=15
    )

    # 4. Parse JSON
    data = response.json()

    if data.get("status") != "success":
        print("ERROR:", data)
        return

    encrypted_seed = data["encrypted_seed"]

    # 5. Save to encrypted_seed.txt (DO NOT commit)
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed saved to encrypted_seed.txt !")


if __name__ == "__main__":
    # ENTER YOUR REAL STUDENT ID HERE
    student_id = "23MH1A4228"

    github_repo_url = "https://github.com/Dhanasirikoppisetti/pki-2fa-microservice"

    request_seed(student_id, github_repo_url)
