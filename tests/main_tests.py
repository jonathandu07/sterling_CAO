# tests\main_tests.py

import subprocess
import os
import datetime

def get_next_log_number(logs_dir, base_name):
    n = 1
    while True:
        fname = f"{base_name}_{n}.txt"
        if not os.path.exists(os.path.join(logs_dir, fname)):
            return n
        n += 1

def main():
    # Dossier des tests (dossier courant = tests)
    tests_dir = os.path.abspath(".")
    logs_dir = os.path.abspath("../logs")
    os.makedirs(logs_dir, exist_ok=True)
    now = datetime.datetime.now()
    d = now.strftime("%d_%m_%Y")
    base_name = f"log_{d}"
    num = get_next_log_number(logs_dir, base_name)
    log_path = os.path.join(logs_dir, f"{base_name}_{num}.txt")

    scripts = [f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")]
    scripts.sort()

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"==== Rapport de tests du {now.strftime('%d/%m/%Y %H:%M:%S')} ====\n")
        log_file.write(f"Tests exécutés ({len(scripts)}) :\n" + "\n".join(scripts) + "\n\n")
        for i, script in enumerate(scripts, 1):
            log_file.write(f"\n\n########## {i}/{len(scripts)} : {script} ##########\n\n")
            cmd = ["python", os.path.join(tests_dir, script)]
            log_file.write(f"Commande lancée : {' '.join(cmd)}\n\n")
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120
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
