from fastapi import FastAPI
from pathlib import Path
import pyexasol
import ssl

app = FastAPI(title="SmartLab AI API")


def get_connection():
    password = Path.home().joinpath(
        ".exasol-starter-kit",
        "credentials",
        "nano_sys_password"
    ).read_text().strip()

    return pyexasol.connect(
        dsn="127.0.0.1:8563",
        user="sys",
        password=password,
        encryption=True,
        websocket_sslopt={"cert_reqs": ssl.CERT_NONE},
    )


@app.get("/")
def home():
    return {
        "message": "SmartLab AI API is running!"
    }


@app.get("/equipment")
def get_equipment():
    conn = get_connection()

    try:
        result = conn.execute("""
            SELECT
                equipment_id,
                name,
                equipment_type,
                availability,
                health_score,
                maintenance_date,
                status
            FROM SMARTLAB.EQUIPMENT
            ORDER BY equipment_id
        """).fetchall()

        columns = [
            "id",
            "name",
            "equipment_type",
            "availability",
            "health_score",
            "maintenance_date",
            "status"
        ]

        equipment = [
            dict(zip(columns, row))
            for row in result
        ]

        return {"equipment": equipment}

    finally:
        conn.close()