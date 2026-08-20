import pyexasol
import ssl
from pathlib import Path

password = Path.home().joinpath(
    ".exasol-starter-kit", "credentials", "nano_sys_password"
).read_text().strip()

conn = pyexasol.connect(
    dsn="127.0.0.1:8563",
    user="sys",
    password=password,
    encryption=True,
    websocket_sslopt={"cert_reqs": ssl.CERT_NONE},
)

sql = Path("database.sql").read_text(encoding="utf-8")

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        print("Executing:", statement[:80].replace("\n", " "))
        conn.execute(statement)

conn.commit()
conn.close()

print("SUCCESS: database.sql loaded into Exasol")
