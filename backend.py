
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
        "message": "SmartLab AI API is running!",
        "database": "Exasol",
        "status": "connected"
    }


# ============================================================
# EQUIPMENT
# EXASOL -> BACKEND -> FRONTEND
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

        # ----------------------------------------------------
        # Check user
        # ----------------------------------------------------

        user = conn.execute(
            """
            SELECT user_id
            FROM SMARTLAB.USERS
            WHERE user_id = {user_id}
            """,
            {
                "user_id": user_id
            }
        ).fetchone()

        if user is None:
            return {
                "success": False,
                "message": "User not found."
            }

        # ----------------------------------------------------
        # Check equipment
        # ----------------------------------------------------

        equipment = conn.execute(
            """
            SELECT name, availability
            FROM SMARTLAB.EQUIPMENT
            WHERE equipment_id = {equipment_id}
            """,
            {
                "equipment_id": equipment_id
            }
        ).fetchone()

        if equipment is None:
            return {
                "success": False,
                "message": "Equipment not found."
            }

        equipment_name = str(equipment[0])
        availability = str(equipment[1])

        if availability != "Available":
            return {
                "success": False,
                "message": (
                    f"{equipment_name} "
                    "is not currently available."
                )
            }

        # ----------------------------------------------------
        # Insert booking
        # ----------------------------------------------------

        conn.execute(
            """
            INSERT INTO SMARTLAB.BOOKINGS
                (
                    user_id,
                    equipment_id,
                    booking_date,
                    start_time,
                    end_time,
                    status
                )
            VALUES
                (
                    {user_id},
                    {equipment_id},
                    {booking_date},
                    {start_time},
                    {end_time},
                    'Confirmed'
                )
            """,
            {
                "user_id": user_id,
                "equipment_id": equipment_id,
                "booking_date": booking_date,
                "start_time": start_time,
                "end_time": end_time
            }
        )

        # ----------------------------------------------------
        # Mark equipment as booked
        # ----------------------------------------------------

        conn.execute(
            """
            UPDATE SMARTLAB.EQUIPMENT
            SET availability = 'Booked'
            WHERE equipment_id = {equipment_id}
            """,
            {
                "equipment_id": equipment_id
            }
        )

        # ----------------------------------------------------
        # Create notification
        # ----------------------------------------------------

        conn.execute(
            """
            INSERT INTO SMARTLAB.NOTIFICATIONS
                (
                    user_id,
                    message,
                    priority,
                    is_read,
                    created_date
                )
            VALUES
                (
                    {user_id},
                    {message},
                    'Medium',
                    FALSE,
                    CURRENT_DATE
                )
            """,
            {
                "user_id": user_id,
                "message": (
                    f"Your {equipment_name} "
                    "booking is confirmed."
                )
            }
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

        # ----------------------------------------------------
        # Check equipment
        # ----------------------------------------------------

        equipment = conn.execute(
            """
            SELECT name
            FROM SMARTLAB.EQUIPMENT
            WHERE equipment_id = {equipment_id}
            """,
            {
                "equipment_id": equipment_id
            }
        ).fetchone()

        if equipment is None:
            return {
                "success": False,
                "message": "Equipment not found."
            }

        equipment_name = str(equipment[0])

        # ----------------------------------------------------
        # Insert issue
        # ----------------------------------------------------

        conn.execute(
            """
            INSERT INTO SMARTLAB.ISSUES
                (
                    equipment_id,
                    reported_by,
                    description,
                    priority,
                    status,
                    reported_date
                )
            VALUES
                (
                    {equipment_id},
                    {reported_by},
                    {description},
                    {priority},
                    'Open',
                    CURRENT_DATE
                )
            """,
            {
                "equipment_id": equipment_id,
                "reported_by": reported_by,
                "description": description,
                "priority": priority
            }
        )

        # ----------------------------------------------------
        # Create notification for lab manager
        # ----------------------------------------------------

        conn.execute(
            """
            INSERT INTO SMARTLAB.NOTIFICATIONS
                (
                    user_id,
                    message,
                    priority,
                    is_read,
                    created_date
                )
            VALUES
                (
                    3,
                    {message},
                    {priority},
                    FALSE,
                    CURRENT_DATE
                )
            """,
            {
                "message": (
                    f"Issue reported for "
                    f"{equipment_name}: {description}"
                ),
                "priority": priority
            }
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
            ORDER BY
                i.reported_date DESC,
                i.issue_id DESC
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


# ============================================================
# GET NOTIFICATIONS
# EXASOL -> BACKEND -> FRONTEND
# ============================================================

@app.get("/notifications")
def get_notifications(user_id: int = 1):

    conn = None

    try:
        conn = get_connection()

        result = conn.execute(
            """
            SELECT
                notification_id,
                message,
                priority,
                is_read,
                created_date
            FROM SMARTLAB.NOTIFICATIONS
            WHERE user_id = {user_id}
            ORDER BY notification_id DESC
            """,
            {
                "user_id": user_id
            }
        ).fetchall()

        notifications = []

        for row in result:

            notification_id = row[0]
            message = row[1]
            priority = row[2]
            is_read = row[3]
            created_date = row[4]

            if str(priority).upper() == "HIGH":
                title = "High Priority Alert"

            elif str(priority).upper() == "MEDIUM":
                title = "SmartLab Update"

            else:
                title = "SmartLab Notification"

            notifications.append({
                "notification_id": str(
                    notification_id
                ),
                "title": title,
                "message": str(message),
                "priority": str(priority),
                "is_read": (
                    str(is_read).upper() == "TRUE"
                ),
                "created_date": str(created_date)
            })

        return {
            "notifications": notifications
        }

    except Exception as e:
        print(
            "NOTIFICATIONS ERROR:",
            repr(e)
        )
        raise

    finally:
        if conn is not None:
            conn.close()


# ============================================================
# MARK NOTIFICATION AS READ
# FRONTEND -> BACKEND -> EXASOL
# ============================================================

@app.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int
):

    conn = None

    try:
        conn = get_connection()

        conn.execute(
            """
            UPDATE SMARTLAB.NOTIFICATIONS
            SET is_read = TRUE
            WHERE notification_id = {notification_id}
            """,
            {
                "notification_id": notification_id
            }
        )

        return {
            "success": True,
            "message": "Notification marked as read."
        }

    except Exception as e:
        print(
            "NOTIFICATION UPDATE ERROR:",
            repr(e)
        )
        raise

    finally:
        if conn is not None:
            conn.close()

