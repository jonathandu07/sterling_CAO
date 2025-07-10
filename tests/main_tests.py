# tests/main_tests.py

import subprocess
import sys
import os
import traceback
import datetime

# Patch sys.path pour tous les tests exécutés directement
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ===== Patch automatique des scripts de test =====

PATCH = (
    "import sys, os\n"
    "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n"
)

def auto_patch_tests(tests_dir):
    """
    Ajoute le patch sys.path au début de chaque script de test s'il n'y est pas déjà.
    """
    patched = []
    for fname in os.listdir(tests_dir):
        if fname.startswith("test_") and fname.endswith(".py"):
            fpath = os.path.join(tests_dir, fname)
            with open(fpath, encoding="utf-8") as f:
                content = f.read()
            # On ne repatche pas si déjà présent (sur une des 2 lignes)
            if PATCH.splitlines()[0] not in content:
                # Ajout du patch tout en haut (juste après un shebang éventuel)
                lines = content.splitlines()
                if lines and lines[0].startswith("#!"):
                    new_content = lines[0] + "\n" + PATCH + "\n" + "\n".join(lines[1:]) + "\n"
                else:
                    new_content = PATCH + "\n" + content
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                patched.append(fname)
    if patched:
        print(f"Patching sys.path dans : {', '.join(patched)}")
    else:
        print("Tous les tests sont déjà patchés.")

def get_next_log_number(logs_dir, base_name):
    n = 1
    while True:
        fname = f"{base_name}_{n}.txt"
        if not os.path.exists(os.path.join(logs_dir, fname)):
            return n
        n += 1

def main():
    # Toujours trouver le dossier des tests et logs même si lancé depuis ailleurs
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.abspath(os.path.join(tests_dir, "../logs"))
    os.makedirs(logs_dir, exist_ok=True)
    now = datetime.datetime.now()
    d = now.strftime("%d_%m_%Y")
    base_name = f"log_{d}"
    num = get_next_log_number(logs_dir, base_name)
    log_path = os.path.join(logs_dir, f"{base_name}_{num}.txt")

    # Patch automatique avant d'exécuter quoi que ce soit
    auto_patch_tests(tests_dir)

    # On ne prend que les scripts de test qui commencent par "test_"
    scripts = [f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")]
    scripts.sort()

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"==== Rapport de tests du {now.strftime('%d/%m/%Y %H:%M:%S')} ====\n")
        log_file.write(f"Tests exécutés ({len(scripts)}) :\n" + "\n".join(scripts) + "\n\n")
        for i, script in enumerate(scripts, 1):
            log_file.write(f"\n\n########## {i}/{len(scripts)} : {script} ##########\n\n")
            # On lance le script de test AVEC le bon interpréteur Python (compatibilité venv)
            cmd = [sys.executable, os.path.join(tests_dir, script)]
            log_file.write(f"Commande lancée : {' '.join(cmd)}\n\n")
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=tests_dir  # Exécution dans le dossier tests
                )
                log_file.write("=== STDOUT ===\n")
                log_file.write(result.stdout)
                log_file.write("\n=== STDERR ===\n")
                log_file.write(result.stderr)
                if result.returncode == 0:
                    log_file.write("\n[OK] Script terminé sans erreur.\n")
                else:
                    log_file.write(f"\n[ERREUR] Code retour : {result.returncode}\n")
            except Exception as e:
                log_file.write(f"\n[EXCEPTION] {e}\n")
            log_file.write("\n" + "="*50 + "\n")

    print(f"Tous les tests sont joués !\nRésultats complets dans : {log_path}")

if __name__ == "__main__":
    main()
