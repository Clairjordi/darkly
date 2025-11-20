Unvalidated Redirect

<a href="index.php?page=redirect&amp;site=facebook" class="icon fa-facebook"></a>
remplacer la valeur du site par n'importe quoi d'autre 
<a href="index.php?page=redirect&amp;site=other" class="icon fa-facebook"></a>

Si le paramètre site (ex : ?page=redirect&site=facebook) est utilisé pour construire une URL de redirection sans validation, un attaquant peut le remplacer par n’importe quel domaine malveillant :