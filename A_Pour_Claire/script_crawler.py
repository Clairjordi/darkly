import subprocess
import sys
from urllib.parse import urljoin

def run_curl(url):
    """Exécute curl pour récupérer le contenu d'une URL."""
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erreur curl pour {url}: {e}")
        return None

def explore_for_readme(base_url, current_path, visited=None):
    """Explore récursivement les répertoires sous .hidden/ et vérifie uniquement les URLs contenant 'README'."""
    if visited is None:
        visited = set()

    dir_url = urljoin(base_url, current_path)
    if dir_url in visited or not dir_url.startswith(base_url):
        return None
    visited.add(dir_url)

    # Récupérer le contenu du répertoire
    content = run_curl(dir_url)
    if content is None:
        return None

    # Parser le contenu pour trouver des liens
    lines = content.split('\n')
    for line in lines:
        if '<a href="' in line:
            start = line.find('<a href="') + len('<a href="')
            end = line.find('"', start)
            if start != -1 and end != -1:
                subpath = line[start:end]
                absolute_url = urljoin(dir_url, subpath)

                if "README" in absolute_url:
                    readme_content = run_curl(absolute_url)
                    if readme_content and "flag" in readme_content.lower():
                        print(f"🚩 Flag trouvé dans: {absolute_url}")
                        print(f"Contenu:{readme_content}")
                        return absolute_url
                    else:
                        print(f"Exploring: {absolute_url}")
                        print(f"Contenu: {readme_content}")
                elif subpath.endswith('/'):
                    result = explore_for_readme(base_url, urljoin(current_path, subpath), visited)
                    if result is not None:
                        return result

    return None


if len(sys.argv ) == 2:
    base_url = f"http://{sys.argv[1]}/.hidden/"
else:
    print("Error: please set the IP address in the script parameter")
    exit(1)

flag_location = explore_for_readme(base_url, "")
if flag_location  is None:
    print("\nAucun flag trouvé dans les URLs contenant 'README' sous .hidden/")

