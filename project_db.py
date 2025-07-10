import sqlite3
from cryptography.fernet import Fernet
import base64
import hashlib

DB_PATH = "projets_cao.db"
TABLE_NAME = "projects"

# GÉNÈRE ET STOCKE TA CLÉ AES quelque part (jamais dans le code prod !)
def get_aes_key(password: str) -> bytes:
    # Derive une clé 32 bytes à partir d’un mot de passe (exemple simple)
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        data BLOB NOT NULL
    )""")
    conn.commit()
    conn.close()

def save_project(name, data_dict, aes_key):
    # Sérialisation et chiffrement
    import json
    f = Fernet(aes_key)
    data = json.dumps(data_dict).encode()
    encrypted_data = f.encrypt(data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"INSERT INTO {TABLE_NAME} (name, data) VALUES (?, ?)", (name, encrypted_data))
    conn.commit()
    conn.close()

def load_projects(aes_key):
    from cryptography.fernet import InvalidToken
    import json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"SELECT id, name, data FROM {TABLE_NAME}")
    projects = []
    f = Fernet(aes_key)
    for pid, name, encrypted_data in c.fetchall():
        try:
            data_json = f.decrypt(encrypted_data)
            data_dict = json.loads(data_json.decode())
        except InvalidToken:
            data_dict = None  # Erreur de clé ou de données
        projects.append({"id": pid, "name": name, "data": data_dict})
    conn.close()
    return projects

def load_project(pid, aes_key):
    from cryptography.fernet import InvalidToken
    import json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"SELECT data FROM {TABLE_NAME} WHERE id=?", (pid,))
    row = c.fetchone()
    if row:
        f = Fernet(aes_key)
        try:
            data_json = f.decrypt(row[0])
            return json.loads(data_json.decode())
        except InvalidToken:
            return None
    return None

# Appelle au lancement du soft
init_db()
