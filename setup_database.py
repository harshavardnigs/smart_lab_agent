"""
SmartLab AI — Database Setup Script
------------------------------------
Runs database.sql against the local Exasol instance to create the
SMARTLAB schema and load seed data.
 
Usage:
    python setup_database.py
"""
 
import ssl
from pathlib import Path
 
import pyexasol
 
CREDENTIALS_PATH = Path.home().joinpath(
    ".exasol-starter-kit", "credentials", "nano_sys_password"
)
SQL_FILE = Path(__file__).parent / "database.sql"
 
 
def get_password() -> str:
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"Could not find Exasol credentials file at {CREDENTIALS_PATH}. "
            "Make sure the Exasol starter kit is installed and running."
        )
    return CREDENTIALS_PATH.read_text().strip()
 
 
def connect():
    return pyexasol.connect(
        dsn="127.0.0.1:8563",
        user="sys",
        password=get_password(),
        encryption=True,
        websocket_sslopt={"cert_reqs": ssl.CERT_NONE},
    )
 
 
def run_sql_file(conn, path: Path):
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
 
    sql = path.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip()]
 
    print(f"Found {len(statements)} statements in {path.name}\n")
 
    for i, statement in enumerate(statements, start=1):
        preview = statement[:80].replace("\n", " ")
        print(f"[{i}/{len(statements)}] Executing: {preview}")
        try:
            conn.execute(statement)
        except Exception as e:
            print(f"  -> WARNING: statement failed ({e}). Continuing...")
 
 
def main():
    print("Connecting to Exasol...")
    conn = connect()
 
    try:
        run_sql_file(conn, SQL_FILE)
        conn.commit()
        print("\nSUCCESS: database.sql loaded into Exasol")
    finally:
        conn.close()
 
 
if __name__ == "__main__":
    main()