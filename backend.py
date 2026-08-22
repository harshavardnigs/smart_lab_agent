
from fastapi import FastAPI
from pathlib import Path
import pyexasol
import ssl

app = FastAPI(title="SmartLab AI API")


# ============================================================
# EXASOL CONNECTION
# ============================================================

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
        schema="SMARTLAB",
    )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "SmartLab AI API is running!"
    }


# ============================================================
# GET EQUIPMENT
# FRONTEND -> BACKEND -> EXASOL -> BACKEND -> FRONTEND
# ============================================================

@app.get("/equipment")
def get_equipment():

    conn = None

    try:
        conn = get_connection()

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

        equipment = []

        for row in result:
            equipment.append({
                "id": str(row[0]),
                "name": str(row[1]),
                "equipment_type": str(row[2]),
                "availability": str(row[3]),
                "health_score": str(row[4]),
                "maintenance_date": str(row[5]),
                "status": str(row[6])
            })

        return {"equipment": equipment}

    except Exception as e:
        print("EQUIPMENT ERROR:", repr(e))
        raise

    finally:
        if conn is not None:
            conn.close()


# ============================================================
# CREATE BOOKING
# FRONTEND -> BACKEND -> EXASOL
# ============================================================

@app.post("/bookings")
def create_booking(
    user_id: int,
    equipment_id: int,
    booking_date: str,
    start_time: str,
    end_time: str
):

    conn = None

    try:
        conn = get_connection()

        # Check whether equipment exists and is available
        equipment = conn.execute(
            """
            SELECT availability
            FROM SMARTLAB.EQUIPMENT
            WHERE equipment_id = ?
            """,
            [equipment_id]
        ).fetchone()

        if equipment is None:
            return {
                "success": False,
                "message": "Equipment not found."
            }

        if str(equipment[0]) != "Available":
            return {
                "success": False,
                "message": "Equipment is not currently available."
            }

        # Insert booking
        conn.execute(
            """
            INSERT INTO SMARTLAB.BOOKINGS
                (user_id, equipment_id, booking_date,
                 start_time, end_time, status)
            VALUES (?, ?, ?, ?, ?, 'Confirmed')
            """,
            [
                user_id,
                equipment_id,
                booking_date,
                start_time,
                end_time
            ]
        )

        # Update equipment availability
        conn.execute(
            """
            UPDATE SMARTLAB.EQUIPMENT
            SET availability = 'Booked'
            WHERE equipment_id = ?
            """,
            [equipment_id]
        )

        return {
            "success": True,
            "message": "Booking created successfully."
        }

    except Exception as e:
        print("BOOKING ERROR:", repr(e))
        raise

    finally:
        if conn is not None:
            conn.close()


# ============================================================
# GET BOOKINGS
# EXASOL -> BACKEND -> FRONTEND
# ============================================================

@app.get("/bookings")
def get_bookings():

    conn = None

    try:
        conn = get_connection()

        result = conn.execute("""
            SELECT
                b.booking_id,
                e.name,
                b.booking_date,
                b.start_time,
                b.end_time,
                b.status
            FROM SMARTLAB.BOOKINGS b
            JOIN SMARTLAB.EQUIPMENT e
                ON b.equipment_id = e.equipment_id
            ORDER BY b.booking_date, b.start_time
        """).fetchall()

        bookings = []

        for row in result:
            bookings.append({
                "booking_id": str(row[0]),
                "equipment": str(row[1]),
                "date": str(row[2]),
                "start_time": str(row[3]),
                "end_time": str(row[4]),
                "status": str(row[5])
            })

        return {"bookings": bookings}

    except Exception as e:
        print("BOOKINGS ERROR:", repr(e))
        raise

    finally:
        if conn is not None:
            conn.close()


# ============================================================
# REPORT ISSUE
# FRONTEND -> BACKEND -> EXASOL
# ============================================================

@app.post("/issues")
def report_issue(
    equipment_id: int,
    reported_by: int,
    description: str,
    priority: str
):

    conn = None

    try:
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO SMARTLAB.ISSUES
                (equipment_id, reported_by, description,
                 priority, status, reported_date)
            VALUES (?, ?, ?, ?, 'Open', CURRENT_DATE)
            """,
            [
                equipment_id,
                reported_by,
                description,
                priority
            ]
        )

        return {
            "success": True,
            "message": "Issue reported successfully."
        }

    except Exception as e:
        print("ISSUE ERROR:", repr(e))
        raise

    finally:
        if conn is not None:
            conn.close()


# ============================================================
# GET ISSUES
# EXASOL -> BACKEND -> FRONTEND
# ============================================================

@app.get("/issues")
def get_issues():

    conn = None

    try:
        conn = get_connection()

        result = conn.execute("""
            SELECT
                i.issue_id,
                e.name,
                i.description,
                i.priority,
                i.status,
                i.reported_date
            FROM SMARTLAB.ISSUES i
            JOIN SMARTLAB.EQUIPMENT e
                ON i.equipment_id = e.equipment_id
            ORDER BY i.reported_date DESC
        """).fetchall()

        issues = []

        for row in result:
            issues.append({
                "issue_id": str(row[0]),
                "equipment": str(row[1]),
                "description": str(row[2]),
                "priority": str(row[3]),
                "status": str(row[4]),
                "reported_date": str(row[5])
            })

        return {"issues": issues}

    except Exception as e:
        print("ISSUES ERROR:", repr(e))
        raise

    finally:
        if conn is not None:
            conn.close()

