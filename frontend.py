import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests


# ============================================================
# SMARTLAB AI
# FRONTEND <-> FASTAPI <-> EXASOL
# ============================================================

API_URL = "http://127.0.0.1:8000"

CURRENT_USER_ID = 1
CURRENT_USER_NAME = "Arun Kumar"


# ============================================================
# API FUNCTIONS
# ============================================================

def get_equipment():
    response = requests.get(
        f"{API_URL}/equipment",
        timeout=10
    )
    response.raise_for_status()
    return response.json()["equipment"]


def get_bookings():
    response = requests.get(
        f"{API_URL}/bookings",
        timeout=10
    )
    response.raise_for_status()
    return response.json()["bookings"]


def create_booking(
    equipment_id,
    booking_date,
    start_time,
    end_time
):
    response = requests.post(
        f"{API_URL}/bookings",
        params={
            "user_id": CURRENT_USER_ID,
            "equipment_id": equipment_id,
            "booking_date": booking_date,
            "start_time": start_time,
            "end_time": end_time
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()


def get_issues():
    response = requests.get(
        f"{API_URL}/issues",
        timeout=10
    )
    response.raise_for_status()
    return response.json()["issues"]


def create_issue(
    equipment_id,
    description,
    priority
):
    response = requests.post(
        f"{API_URL}/issues",
        params={
            "equipment_id": equipment_id,
            "reported_by": CURRENT_USER_ID,
            "description": description,
            "priority": priority
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()


def get_notifications():
    response = requests.get(
        f"{API_URL}/notifications",
        params={
            "user_id": CURRENT_USER_ID
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()["notifications"]


def mark_notification_read(notification_id):
    response = requests.put(
        f"{API_URL}/notifications/{notification_id}/read",
        timeout=10
    )

    response.raise_for_status()
    return response.json()


# ============================================================
# API ERROR HANDLING
# ============================================================

def api_error_message(error):

    if isinstance(
        error,
        requests.exceptions.ConnectionError
    ):
        return (
            "Could not connect to the SmartLab backend.\n\n"
            "Make sure backend.py is running."
        )

    if isinstance(
        error,
        requests.exceptions.Timeout
    ):
        return (
            "The SmartLab backend took too long "
            "to respond."
        )

    if isinstance(
        error,
        requests.exceptions.HTTPError
    ):
        return (
            "The backend returned an error.\n\n"
            f"Status: {error.response.status_code}\n"
            f"Response: {error.response.text}"
        )

    return f"Unexpected error:\n\n{error}"


# ============================================================
# COLORS
# ============================================================

NAVY = "#172554"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#EA580C"

LIGHT_RED = "#FEE2E2"
LIGHT_ORANGE = "#FFEDD5"

TEXT = "#172033"
MUTED = "#64748B"
WHITE = "#FFFFFF"
BORDER = "#E2E8F0"
BG = "#F4F7FB"

FONT = "Segoe UI"


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()

root.title("SmartLab AI")

root.geometry("1400x850")

root.minsize(
    1100,
    700
)

root.configure(
    bg=BG
)


# ============================================================
# GLOBAL DATA
# ============================================================

equipment = []
bookings = []
issues = []
notifications = []


# ============================================================
# HELPERS
# ============================================================

def clear_content():

    for widget in content.winfo_children():
        widget.destroy()


def create_button(
    parent,
    text,
    command,
    bg=BLUE,
    fg=WHITE
):

    return tk.Button(
        parent,
        text=text,
        command=command,
        font=(FONT, 10, "bold"),
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=9
    )


def card(parent):

    return tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )


def section_title(
    parent,
    title,
    subtitle=None
):

    tk.Label(
        parent,
        text=title,
        font=(FONT, 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    if subtitle:

        tk.Label(
            parent,
            text=subtitle,
            font=(FONT, 10),
            bg=BG,
            fg=MUTED
        ).pack(
            anchor="w",
            pady=(3, 15)
        )


# ============================================================
# REFRESH EVERYTHING
# ============================================================

def refresh_data():

    global equipment
    global bookings
    global issues
    global notifications

    try:

        equipment = get_equipment()

        bookings = get_bookings()

        issues = get_issues()

        notifications = get_notifications()

    except Exception as e:

        print(
            "DATA REFRESH ERROR:",
            repr(e)
        )


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    refresh_data()

    clear_content()

    available_count = sum(
        1
        for item in equipment
        if item["availability"] == "Available"
    )

    open_issues = sum(
        1
        for issue in issues
        if issue["status"].lower() == "open"
    )

    unread_notifications = sum(
        1
        for notification in notifications
        if not notification["is_read"]
    )

    tk.Label(
        content,
        text=f"Good evening, {CURRENT_USER_NAME} 👋",
        font=(FONT, 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        content,
        text="Here's what's happening in your laboratory today.",
        font=(FONT, 11),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        pady=(2, 22)
    )

    stats = tk.Frame(
        content,
        bg=BG
    )

    stats.pack(
        fill="x"
    )

    stats_data = [
        (
            "🔬",
            "Equipment",
            str(len(equipment)),
            BLUE
        ),
        (
            "🟢",
            "Available",
            str(available_count),
            GREEN
        ),
        (
            "🚨",
            "Open Issues",
            str(open_issues),
            RED
        ),
        (
            "📅",
            "Bookings",
            str(len(bookings)),
            PURPLE
        )
    ]

    for icon, title, value, color in stats_data:

        c = card(stats)

        c.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        tk.Label(
            c,
            text=icon,
            font=(FONT, 22),
            bg=WHITE
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 0)
        )

        tk.Label(
            c,
            text=value,
            font=(FONT, 24, "bold"),
            bg=WHITE,
            fg=color
        ).pack(
            anchor="w",
            padx=18
        )

        tk.Label(
            c,
            text=title,
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 15)
        )

    # AI INSIGHT

    low_health = None

    if equipment:

        low_health = min(
            equipment,
            key=lambda x: float(
                x["health_score"]
            )
        )

    ai_frame = tk.Frame(
        content,
        bg="#EEF2FF",
        highlightbackground="#C7D2FE",
        highlightthickness=1
    )

    ai_frame.pack(
        fill="x",
        pady=25
    )

    tk.Label(
        ai_frame,
        text="🤖  AI LAB INSIGHT",
        font=(FONT, 11, "bold"),
        bg="#EEF2FF",
        fg=PURPLE
    ).pack(
        anchor="w",
        padx=22,
        pady=(18, 5)
    )

    if low_health:

        tk.Label(
            ai_frame,
            text=(
                f'{low_health["name"]} has the lowest '
                f'health score at '
                f'{low_health["health_score"]}%.'
            ),
            font=(FONT, 11, "bold"),
            bg="#EEF2FF",
            fg=TEXT
        ).pack(
            anchor="w",
            padx=22
        )

        tk.Label(
            ai_frame,
            text=(
                "Recommendation: Check its maintenance "
                f"status. Current status: "
                f'{low_health["status"]}.'
            ),
            font=(FONT, 10),
            bg="#EEF2FF",
            fg=MUTED
        ).pack(
            anchor="w",
            padx=22,
            pady=(5, 18)
        )

    # EQUIPMENT + BOOKINGS

    lower = tk.Frame(
        content,
        bg=BG
    )

    lower.pack(
        fill="both",
        expand=True
    )

    left = tk.Frame(
        lower,
        bg=BG
    )

    left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    tk.Label(
        left,
        text="Equipment",
        font=(FONT, 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=(0, 12)
    )

    for item in equipment[:5]:

        c = tk.Frame(
            left,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        c.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            c,
            text=item["name"],
            font=(FONT, 11, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            side="left",
            padx=15,
            pady=13
        )

        availability = item["availability"]

        if availability == "Available":
            color = GREEN
        elif availability == "Booked":
            color = ORANGE
        else:
            color = RED

        tk.Label(
            c,
            text=availability,
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=color
        ).pack(
            side="right",
            padx=15
        )

    right = tk.Frame(
        lower,
        bg=BG
    )

    right.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(12, 0)
    )

    tk.Label(
        right,
        text="Upcoming Bookings",
        font=(FONT, 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=(0, 12)
    )

    for booking in bookings[:5]:

        c = tk.Frame(
            right,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        c.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            c,
            text="📅",
            font=(FONT, 18),
            bg=WHITE
        ).pack(
            side="left",
            padx=12
        )

        info = tk.Frame(
            c,
            bg=WHITE
        )

        info.pack(
            side="left",
            pady=10
        )

        tk.Label(
            info,
            text=booking["equipment"],
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w"
        )

        tk.Label(
            info,
            text=(
                f'{booking["date"]} • '
                f'{booking["start_time"]} - '
                f'{booking["end_time"]}'
            ),
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w"
        )


# ============================================================
# EQUIPMENT
# ============================================================

def show_equipment():

    refresh_data()

    clear_content()

    section_title(
        content,
        "🔬 Equipment",
        "Equipment loaded directly from Exasol."
    )

    toolbar = tk.Frame(
        content,
        bg=BG
    )

    toolbar.pack(
        fill="x",
        pady=(0, 15)
    )

    search = tk.Entry(
        toolbar,
        font=(FONT, 10),
        bg=WHITE,
        fg=TEXT,
        relief="solid",
        bd=1
    )

    search.pack(
        side="left",
        ipadx=15,
        ipady=8
    )

    equipment_container = tk.Frame(
        content,
        bg=BG
    )

    equipment_container.pack(
        fill="both",
        expand=True
    )

    def render(items):

        for widget in equipment_container.winfo_children():
            widget.destroy()

        for item in items:

            c = tk.Frame(
                equipment_container,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            c.pack(
                fill="x",
                pady=6
            )

            top = tk.Frame(
                c,
                bg=WHITE
            )

            top.pack(
                fill="x",
                padx=20,
                pady=(15, 5)
            )

            tk.Label(
                top,
                text=item["name"],
                font=(FONT, 14, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(
                side="left"
            )

            availability = item["availability"]

            if availability == "Available":
                status_color = GREEN
            elif availability == "Booked":
                status_color = ORANGE
            else:
                status_color = RED

            tk.Label(
                top,
                text=f"● {availability}",
                font=(FONT, 10, "bold"),
                bg=WHITE,
                fg=status_color
            ).pack(
                side="right"
            )

            tk.Label(
                c,
                text=item["equipment_type"],
                font=(FONT, 9),
                bg=WHITE,
                fg=MUTED
            ).pack(
                anchor="w",
                padx=20
            )

            details = tk.Frame(
                c,
                bg=WHITE
            )

            details.pack(
                fill="x",
                padx=20,
                pady=12
            )

            health = float(
                item["health_score"]
            )

            tk.Label(
                details,
                text=f"Health: {health:.0f}%",
                font=(FONT, 10, "bold"),
                bg=WHITE,
                fg=(
                    GREEN
                    if health >= 80
                    else RED
                )
            ).pack(
                side="left",
                padx=(0, 30)
            )

            tk.Label(
                details,
                text=(
                    f'Maintenance: '
                    f'{item["maintenance_date"]}'
                ),
                font=(FONT, 9),
                bg=WHITE,
                fg=MUTED
            ).pack(
                side="left"
            )

            if availability == "Available":

                create_button(
                    details,
                    "Book",
                    lambda x=item: open_booking_window(x),
                    BLUE
                ).pack(
                    side="right"
                )

    def filter_equipment():

        query = (
            search.get()
            .lower()
            .strip()
        )

        filtered = [
            item
            for item in equipment
            if (
                query in item["name"].lower()
                or query in item[
                    "equipment_type"
                ].lower()
            )
        ]

        render(filtered)

    create_button(
        toolbar,
        "Search",
        filter_equipment,
        BLUE
    ).pack(
        side="left",
        padx=8
    )

    create_button(
        toolbar,
        "Refresh",
        show_equipment,
        GREEN
    ).pack(
        side="left"
    )

    render(equipment)


# ============================================================
# BOOKING WINDOW
# ============================================================

def open_booking_window(item):

    if item["availability"] != "Available":

        messagebox.showwarning(
            "Unavailable",
            "This equipment is not currently available."
        )

        return

    window = tk.Toplevel(root)

    window.title("Book Equipment")

    window.geometry("430x520")

    window.configure(
        bg=BG
    )

    window.resizable(
        False,
        False
    )

    tk.Label(
        window,
        text="📅 Book Equipment",
        font=(FONT, 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        window,
        text=item["name"],
        font=(FONT, 12, "bold"),
        bg=BG,
        fg=BLUE
    ).pack(
        pady=(0, 20)
    )

    form = tk.Frame(
        window,
        bg=WHITE
    )

    form.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    tk.Label(
        form,
        text="Date (YYYY-MM-DD)",
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    date_entry = tk.Entry(
        form,
        font=(FONT, 11),
        relief="solid",
        bd=1
    )

    date_entry.pack(
        fill="x",
        padx=20,
        ipady=7
    )

    date_entry.insert(
        0,
        datetime.now().strftime(
            "%Y-%m-%d"
        )
    )

    tk.Label(
        form,
        text="Start Time (HH:MM)",
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    start_entry = tk.Entry(
        form,
        font=(FONT, 11),
        relief="solid",
        bd=1
    )

    start_entry.pack(
        fill="x",
        padx=20,
        ipady=7
    )

    start_entry.insert(
        0,
        "10:00"
    )

    tk.Label(
        form,
        text="End Time (HH:MM)",
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    end_entry = tk.Entry(
        form,
        font=(FONT, 11),
        relief="solid",
        bd=1
    )

    end_entry.pack(
        fill="x",
        padx=20,
        ipady=7
    )

    end_entry.insert(
        0,
        "11:00"
    )

    def submit_booking():

        booking_date = (
            date_entry.get().strip()
        )

        start_time = (
            start_entry.get().strip()
        )

        end_time = (
            end_entry.get().strip()
        )

        if not booking_date or not start_time or not end_time:

            messagebox.showwarning(
                "Missing information",
                "Please fill in all booking fields."
            )

            return

        try:

            result = create_booking(
                int(item["id"]),
                booking_date,
                start_time,
                end_time
            )

            if result.get("success"):

                messagebox.showinfo(
                    "Booking Confirmed",
                    (
                        f'{item["name"]} has been '
                        "booked successfully."
                    )
                )

                window.destroy()

                show_bookings()

            else:

                messagebox.showwarning(
                    "Booking Failed",
                    result.get(
                        "message",
                        "The booking could not be created."
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Booking Error",
                api_error_message(e)
            )

    create_button(
        form,
        "Confirm Booking",
        submit_booking,
        BLUE
    ).pack(
        pady=25
    )


# ============================================================
# BOOKINGS
# ============================================================

def show_bookings():

    refresh_data()

    clear_content()

    section_title(
        content,
        "📅 Bookings",
        "Bookings loaded directly from Exasol."
    )

    if not bookings:

        tk.Label(
            content,
            text="No bookings found.",
            font=(FONT, 12),
            bg=BG,
            fg=MUTED
        ).pack(
            pady=40
        )

    else:

        for booking in bookings:

            c = tk.Frame(
                content,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            c.pack(
                fill="x",
                pady=7
            )

            tk.Label(
                c,
                text="📅",
                font=(FONT, 25),
                bg=WHITE
            ).pack(
                side="left",
                padx=20,
                pady=18
            )

            info = tk.Frame(
                c,
                bg=WHITE
            )

            info.pack(
                side="left",
                pady=15
            )

            tk.Label(
                info,
                text=booking["equipment"],
                font=(FONT, 13, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(
                anchor="w"
            )

            tk.Label(
                info,
                text=(
                    f'{booking["date"]} • '
                    f'{booking["start_time"]} - '
                    f'{booking["end_time"]}'
                ),
                font=(FONT, 10),
                bg=WHITE,
                fg=MUTED
            ).pack(
                anchor="w",
                pady=3
            )

            status = booking["status"]

            tk.Label(
                c,
                text=f"● {status}",
                font=(FONT, 10, "bold"),
                bg=WHITE,
                fg=(
                    GREEN
                    if status == "Confirmed"
                    else RED
                )
            ).pack(
                side="right",
                padx=25
            )

    create_button(
        content,
        "Refresh Bookings",
        show_bookings,
        GREEN
    ).pack(
        anchor="e",
        pady=15
    )


# ============================================================
# ISSUES
# ============================================================

def show_issues():

    refresh_data()

    clear_content()

    section_title(
        content,
        "🚨 Issues",
        "Issues loaded directly from Exasol."
    )

    create_button(
        content,
        "+ Report New Issue",
        open_issue_window,
        RED
    ).pack(
        anchor="e",
        pady=(0, 15)
    )

    if not issues:

        tk.Label(
            content,
            text="No issues reported.",
            font=(FONT, 12),
            bg=BG,
            fg=MUTED
        ).pack(
            pady=40
        )

        return

    for issue in issues:

        issue_frame = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground="#FECACA",
            highlightthickness=1
        )

        issue_frame.pack(
            fill="x",
            pady=6
        )

        tk.Label(
            issue_frame,
            text=f'⚠  {issue["equipment"]}',
            font=(FONT, 14, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        tk.Label(
            issue_frame,
            text=issue["description"],
            font=(FONT, 10),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=20
        )

        bottom = tk.Frame(
            issue_frame,
            bg=WHITE
        )

        bottom.pack(
            fill="x",
            padx=20,
            pady=15
        )

        priority = issue["priority"]

        tk.Label(
            bottom,
            text=priority.upper(),
            font=(FONT, 9, "bold"),
            bg=(
                LIGHT_RED
                if priority.lower() == "high"
                else LIGHT_ORANGE
            ),
            fg=(
                RED
                if priority.lower() == "high"
                else ORANGE
            ),
            padx=8,
            pady=4
        ).pack(
            side="left"
        )

        tk.Label(
            bottom,
            text=f'Status: {issue["status"]}',
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=(
                RED
                if issue["status"].lower() == "open"
                else GREEN
            )
        ).pack(
            side="left",
            padx=15
        )

        tk.Label(
            bottom,
            text=f'Reported: {issue["reported_date"]}',
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(
            side="right"
        )


# ============================================================
# REPORT ISSUE WINDOW
# ============================================================

def open_issue_window():

    refresh_data()

    window = tk.Toplevel(root)

    window.title(
        "Report Issue"
    )

    window.geometry(
        "500x500"
    )

    window.configure(
        bg=BG
    )

    window.resizable(
        False,
        False
    )

    tk.Label(
        window,
        text="🚨 Report Equipment Issue",
        font=(FONT, 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=(25, 20)
    )

    form = tk.Frame(
        window,
        bg=WHITE
    )

    form.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    tk.Label(
        form,
        text="Equipment",
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    equipment_names = [
        item["name"]
        for item in equipment
    ]

    equipment_box = tk.StringVar()

    equipment_dropdown = tk.OptionMenu(
        form,
        equipment_box,
        *equipment_names
    )

    equipment_dropdown.config(
        font=(FONT, 10),
        bg="#F8FAFC",
        relief="solid",
        bd=1
    )

    equipment_dropdown.pack(
        fill="x",
        padx=20
    )

    if equipment_names:
        equipment_box.set(
            equipment_names[0]
        )

    tk.Label(
        form,
        text="Priority",
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    priority_box = tk.StringVar(
        value="High"
    )

    priority_dropdown = tk.OptionMenu(
        form,
        priority_box,
        "Low",
        "Medium",
        "High"
    )

    priority_dropdown.config(
        font=(FONT, 10),
        bg="#F8FAFC",
        relief="solid",
        bd=1
    )

    priority_dropdown.pack(
        fill="x",
        padx=20
    )

    tk.Label(
        form,
        text="Description",
        font=(FONT, 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )

    description = tk.Text(
        form,
        height=5,
        font=(FONT, 10),
        relief="solid",
        bd=1
    )

    description.pack(
        fill="x",
        padx=20
    )

    def submit_issue():

        selected_name = (
            equipment_box.get()
        )

        description_text = (
            description.get(
                "1.0",
                "end"
            ).strip()
        )

        if not selected_name:

            messagebox.showwarning(
                "Missing information",
                "Please select equipment."
            )

            return

        if not description_text:

            messagebox.showwarning(
                "Missing information",
                "Please describe the issue."
            )

            return

        selected_equipment = next(
            (
                item
                for item in equipment
                if item["name"] == selected_name
            ),
            None
        )

        if selected_equipment is None:

            messagebox.showerror(
                "Error",
                "Equipment could not be found."
            )

            return

        try:

            result = create_issue(
                int(
                    selected_equipment["id"]
                ),
                description_text,
                priority_box.get()
            )

            if result.get("success"):

                messagebox.showinfo(
                    "Issue Reported",
                    "The issue has been saved to Exasol."
                )

                window.destroy()

                show_issues()

            else:

                messagebox.showwarning(
                    "Issue Failed",
                    result.get(
                        "message",
                        "The issue could not be saved."
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Issue Error",
                api_error_message(e)
            )

    create_button(
        form,
        "Submit Issue",
        submit_issue,
        RED
    ).pack(
        pady=20
    )


# ============================================================
# NOTIFICATIONS
# ============================================================

def show_notifications():

    refresh_data()

    clear_content()

    section_title(
        content,
        "🔔 Notifications",
        "Notifications loaded directly from Exasol."
    )

    if not notifications:

        tk.Label(
            content,
            text="No notifications.",
            font=(FONT, 12),
            bg=BG,
            fg=MUTED
        ).pack(
            pady=40
        )

        return

    for notification in notifications:

        c = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        c.pack(
            fill="x",
            pady=6
        )

        priority = notification["priority"]

        color = (
            RED
            if priority == "High"
            else BLUE
        )

        tk.Label(
            c,
            text="●",
            font=(FONT, 15),
            bg=WHITE,
            fg=color
        ).pack(
            side="left",
            padx=20
        )

        info = tk.Frame(
            c,
            bg=WHITE
        )

        info.pack(
            side="left",
            pady=15
        )

        tk.Label(
            info,
            text=notification["title"],
            font=(FONT, 11, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w"
        )

        tk.Label(
            info,
            text=notification["message"],
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w",
            pady=3
        )

        tk.Label(
            info,
            text=(
                f'Priority: {priority} • '
                f'{notification["created_date"]}'
            ),
            font=(FONT, 8),
            bg=WHITE,
            fg=MUTED
        ).pack(
            anchor="w"
        )

        if not notification["is_read"]:

            create_button(
                c,
                "Mark Read",
                lambda x=notification[
                    "notification_id"
                ]: mark_read_and_refresh(x),
                GREEN
            ).pack(
                side="right",
                padx=20
            )


def mark_read_and_refresh(
    notification_id
):

    try:

        result = mark_notification_read(
            int(notification_id)
        )

        if result.get("success"):

            show_notifications()

        else:

            messagebox.showwarning(
                "Error",
                "Could not mark notification as read."
            )

    except Exception as e:

        messagebox.showerror(
            "Notification Error",
            api_error_message(e)
        )


# ============================================================
# AI PAGE
# ============================================================

def show_ai():

    refresh_data()

    clear_content()

    tk.Label(
        content,
        text="🤖 Lab AI",
        font=(FONT, 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        content,
        text="Your intelligent laboratory assistant",
        font=(FONT, 11),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        pady=(2, 20)
    )

    chat = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    chat.pack(
        fill="both",
        expand=True
    )

    messages = tk.Text(
        chat,
        font=(FONT, 11),
        bg=WHITE,
        fg=TEXT,
        relief="flat",
        padx=25,
        pady=25,
        wrap="word"
    )

    messages.pack(
        fill="both",
        expand=True
    )

    messages.insert(
        "end",
        "🤖 Lab AI\n\n"
        "The AI model is not connected yet.\n\n"
        "The SmartLab frontend/backend/database "
        "connection is ready.\n\n"
        "Next step: connect the actual AI model "
        "to the backend.\n"
    )

    messages.config(
        state="disabled"
    )


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    root,
    bg=NAVY,
    width=245
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(
    False
)

logo = tk.Frame(
    sidebar,
    bg=NAVY
)

logo.pack(
    fill="x",
    padx=25,
    pady=28
)

tk.Label(
    logo,
    text="🧪",
    font=(FONT, 25),
    bg=NAVY,
    fg=WHITE
).pack(
    side="left"
)

tk.Label(
    logo,
    text="SmartLab",
    font=(FONT, 20, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(
    side="left",
    padx=8
)

tk.Label(
    sidebar,
    text="AI-POWERED LAB MANAGEMENT",
    font=(FONT, 8, "bold"),
    bg=NAVY,
    fg="#93C5FD"
).pack(
    anchor="w",
    padx=28,
    pady=(0, 25)
)


def nav_button(
    text,
    command
):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        font=(FONT, 10, "bold"),
        bg=NAVY,
        fg="#CBD5E1",
        activebackground="#1E3A8A",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        padx=28,
        pady=13,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        padx=10,
        pady=2
    )

    return button


nav_button(
    "🏠   Dashboard",
    show_dashboard
)

nav_button(
    "🔬   Equipment",
    show_equipment
)

nav_button(
    "📅   Bookings",
    show_bookings
)

nav_button(
    "🚨   Issues",
    show_issues
)

nav_button(
    "🔔   Notifications",
    show_notifications
)

nav_button(
    "🤖   Lab AI",
    show_ai
)


# ============================================================
# PROFILE
# ============================================================

profile = tk.Frame(
    sidebar,
    bg="#1E3A8A"
)

profile.pack(
    side="bottom",
    fill="x",
    padx=12,
    pady=15
)

tk.Label(
    profile,
    text="AR",
    font=(FONT, 12, "bold"),
    bg=BLUE,
    fg=WHITE,
    width=3,
    height=1
).pack(
    side="left",
    padx=12,
    pady=12
)

profile_info = tk.Frame(
    profile,
    bg="#1E3A8A"
)

profile_info.pack(
    side="left",
    pady=10
)

tk.Label(
    profile_info,
    text=CURRENT_USER_NAME,
    font=(FONT, 9, "bold"),
    bg="#1E3A8A",
    fg=WHITE
).pack(
    anchor="w"
)

tk.Label(
    profile_info,
    text="Student",
    font=(FONT, 8),
    bg="#1E3A8A",
    fg="#BFDBFE"
).pack(
    anchor="w"
)


# ============================================================
# MAIN CONTENT
# ============================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    side="right",
    fill="both",
    expand=True
)

header = tk.Frame(
    main,
    bg=WHITE,
    height=70,
    highlightbackground=BORDER,
    highlightthickness=1
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)

tk.Label(
    header,
    text="SMARTLAB AI",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    side="left",
    padx=30
)

tk.Label(
    header,
    text="● Lab Online",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=GREEN
).pack(
    side="right",
    padx=30
)

content = tk.Frame(
    main,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=30
)


# ============================================================
# START
# ============================================================

show_dashboard()

root.mainloop()