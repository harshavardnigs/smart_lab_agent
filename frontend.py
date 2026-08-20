import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ============================================================
# SMARTLAB AI — FRONTEND PROTOTYPE
# College Laboratory Management System
# ============================================================

root = tk.Tk()
root.title("SmartLab AI")
root.geometry("1400x850")
root.minsize(1100, 700)
root.configure(bg="#F4F7FB")

# ---------------- COLORS ----------------

NAVY = "#172554"
BLUE = "#2563EB"
LIGHT_BLUE = "#EFF6FF"
PURPLE = "#7C3AED"
GREEN = "#16A34A"
LIGHT_GREEN = "#DCFCE7"
RED = "#DC2626"
LIGHT_RED = "#FEE2E2"
ORANGE = "#EA580C"
LIGHT_ORANGE = "#FFEDD5"
TEXT = "#172033"
MUTED = "#64748B"
WHITE = "#FFFFFF"
BORDER = "#E2E8F0"
BG = "#F4F7FB"

# ---------------- SAMPLE DATA ----------------

equipment = [
    {
        "id": 1,
        "name": "Oscilloscope 01",
        "type": "Oscilloscope",
        "availability": "Available",
        "health": 94,
        "maintenance": "15 Sep 2026",
        "status": "Operational"
    },
    {
        "id": 2,
        "name": "Oscilloscope 02",
        "type": "Oscilloscope",
        "availability": "Booked",
        "health": 91,
        "maintenance": "10 Oct 2026",
        "status": "Operational"
    },
    {
        "id": 3,
        "name": "Power Supply 01",
        "type": "Power Supply",
        "availability": "Unavailable",
        "health": 63,
        "maintenance": "25 Aug 2026",
        "status": "Maintenance"
    },
    {
        "id": 4,
        "name": "Function Generator 01",
        "type": "Function Generator",
        "availability": "Available",
        "health": 88,
        "maintenance": "05 Nov 2026",
        "status": "Operational"
    },
    {
        "id": 5,
        "name": "Digital Multimeter 01",
        "type": "Multimeter",
        "availability": "Available",
        "health": 97,
        "maintenance": "15 Jan 2027",
        "status": "Operational"
    }
]

bookings = [
    {
        "equipment": "Oscilloscope 01",
        "date": "20 Aug 2026",
        "time": "10:00 - 11:00",
        "status": "Confirmed"
    },
    {
        "equipment": "Oscilloscope 02",
        "date": "20 Aug 2026",
        "time": "14:00 - 15:00",
        "status": "Confirmed"
    }
]

notifications = [
    {
        "title": "Maintenance Alert",
        "message": "Power Supply 01 requires maintenance.",
        "priority": "High"
    },
    {
        "title": "Booking Confirmed",
        "message": "Your Oscilloscope 01 booking is confirmed.",
        "priority": "Medium"
    }
]

# ---------------- FONTS ----------------

FONT = "Segoe UI"

# ---------------- HELPER FUNCTIONS ----------------

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def create_button(parent, text, command, bg=BLUE, fg=WHITE):
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


def card(parent, width=250, height=120):
    frame = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    return frame


def section_title(parent, title, subtitle=None):
    tk.Label(
        parent,
        text=title,
        font=(FONT, 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w")

    if subtitle:
        tk.Label(
            parent,
            text=subtitle,
            font=(FONT, 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 15))


# ---------------- DASHBOARD ----------------

def show_dashboard():

    clear_content()

    tk.Label(
        content,
        text="Good evening, Arun 👋",
        font=(FONT, 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Here's what's happening in your laboratory today.",
        font=(FONT, 11),
        bg=BG,
        fg=MUTED
    ).pack(anchor="w", pady=(2, 22))

    # Statistics
    stats = tk.Frame(content, bg=BG)
    stats.pack(fill="x")

    stats_data = [
        ("🔬", "Equipment", "5", BLUE),
        ("🟢", "Available", "3", GREEN),
        ("🚨", "Open Issues", "1", RED),
        ("🔔", "Notifications", "2", PURPLE)
    ]

    for icon, title, value, color in stats_data:

        c = card(stats)
        c.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(
            c,
            text=icon,
            font=(FONT, 22),
            bg=WHITE
        ).pack(anchor="w", padx=18, pady=(15, 0))

        tk.Label(
            c,
            text=value,
            font=(FONT, 24, "bold"),
            bg=WHITE,
            fg=color
        ).pack(anchor="w", padx=18)

        tk.Label(
            c,
            text=title,
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", padx=18, pady=(0, 15))

    # AI insight
    ai_frame = tk.Frame(
        content,
        bg="#EEF2FF",
        highlightbackground="#C7D2FE",
        highlightthickness=1
    )
    ai_frame.pack(fill="x", pady=25)

    tk.Label(
        ai_frame,
        text="🤖  AI LAB INSIGHT",
        font=(FONT, 11, "bold"),
        bg="#EEF2FF",
        fg=PURPLE
    ).pack(anchor="w", padx=22, pady=(18, 5))

    tk.Label(
        ai_frame,
        text="Power Supply 01 has a health score of 63% and an open high-priority issue.",
        font=(FONT, 11, "bold"),
        bg="#EEF2FF",
        fg=TEXT
    ).pack(anchor="w", padx=22)

    tk.Label(
        ai_frame,
        text="Recommendation: Keep the equipment unavailable until maintenance is completed.",
        font=(FONT, 10),
        bg="#EEF2FF",
        fg=MUTED
    ).pack(anchor="w", padx=22, pady=(5, 18))

    # Lower section
    lower = tk.Frame(content, bg=BG)
    lower.pack(fill="both", expand=True)

    # Equipment preview
    left = tk.Frame(lower, bg=BG)
    left.pack(side="left", fill="both", expand=True, padx=(0, 12))

    tk.Label(
        left,
        text="Equipment",
        font=(FONT, 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", pady=(0, 12))

    for item in equipment[:3]:

        c = tk.Frame(
            left,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        c.pack(fill="x", pady=5)

        tk.Label(
            c,
            text=item["name"],
            font=(FONT, 11, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(side="left", padx=15, pady=13)

        color = GREEN if item["availability"] == "Available" else (
            RED if item["availability"] == "Unavailable" else ORANGE
        )

        tk.Label(
            c,
            text=item["availability"],
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=color
        ).pack(side="right", padx=15)

    # Bookings
    right = tk.Frame(lower, bg=BG)
    right.pack(side="right", fill="both", expand=True, padx=(12, 0))

    tk.Label(
        right,
        text="Upcoming Bookings",
        font=(FONT, 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", pady=(0, 12))

    for booking in bookings:

        c = tk.Frame(
            right,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        c.pack(fill="x", pady=5)

        tk.Label(
            c,
            text="📅",
            font=(FONT, 18),
            bg=WHITE
        ).pack(side="left", padx=12)

        info = tk.Frame(c, bg=WHITE)
        info.pack(side="left", pady=10)

        tk.Label(
            info,
            text=booking["equipment"],
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f'{booking["date"]}  •  {booking["time"]}',
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")


# ---------------- EQUIPMENT PAGE ----------------

def show_equipment():

    clear_content()

    section_title(
        content,
        "🔬 Equipment",
        "View laboratory equipment, availability and health."
    )

    toolbar = tk.Frame(content, bg=BG)
    toolbar.pack(fill="x", pady=(0, 15))

    search = tk.Entry(
        toolbar,
        font=(FONT, 10),
        bg=WHITE,
        fg=TEXT,
        relief="solid",
        bd=1
    )
    search.pack(side="left", ipadx=15, ipady=8)

    create_button(
        toolbar,
        "Search",
        lambda: filter_equipment(search.get()),
        BLUE
    ).pack(side="left", padx=8)

    equipment_container = tk.Frame(content, bg=BG)
    equipment_container.pack(fill="both", expand=True)

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
            c.pack(fill="x", pady=6)

            top = tk.Frame(c, bg=WHITE)
            top.pack(fill="x", padx=20, pady=(15, 5))

            tk.Label(
                top,
                text=item["name"],
                font=(FONT, 14, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(side="left")

            status_color = (
                GREEN if item["availability"] == "Available"
                else ORANGE if item["availability"] == "Booked"
                else RED
            )

            tk.Label(
                top,
                text=f'● {item["availability"]}',
                font=(FONT, 10, "bold"),
                bg=WHITE,
                fg=status_color
            ).pack(side="right")

            tk.Label(
                c,
                text=item["type"],
                font=(FONT, 9),
                bg=WHITE,
                fg=MUTED
            ).pack(anchor="w", padx=20)

            details = tk.Frame(c, bg=WHITE)
            details.pack(fill="x", padx=20, pady=12)

            tk.Label(
                details,
                text=f'Health: {item["health"]}%',
                font=(FONT, 10, "bold"),
                bg=WHITE,
                fg=GREEN if item["health"] >= 80 else RED
            ).pack(side="left", padx=(0, 30))

            tk.Label(
                details,
                text=f'Maintenance: {item["maintenance"]}',
                font=(FONT, 9),
                bg=WHITE,
                fg=MUTED
            ).pack(side="left")

            if item["availability"] == "Available":
                create_button(
                    details,
                    "Book",
                    lambda x=item: book_equipment(x),
                    BLUE
                ).pack(side="right")

    def filter_equipment(query):

        query = query.lower()

        filtered = [
            item for item in equipment
            if query in item["name"].lower()
            or query in item["type"].lower()
        ]

        render(filtered)

    render(equipment)


# ---------------- BOOK EQUIPMENT ----------------

def book_equipment(item):

    if item["availability"] != "Available":
        messagebox.showwarning(
            "Unavailable",
            "This equipment is not currently available."
        )
        return

    messagebox.showinfo(
        "Booking",
        f'{item["name"]} is available.\n\n'
        "Booking form will be connected to the database next."
    )


# ---------------- BOOKINGS PAGE ----------------

def show_bookings():

    clear_content()

    section_title(
        content,
        "📅 Bookings",
        "Your upcoming laboratory equipment reservations."
    )

    for booking in bookings:

        c = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        c.pack(fill="x", pady=7)

        tk.Label(
            c,
            text="📅",
            font=(FONT, 25),
            bg=WHITE
        ).pack(side="left", padx=20, pady=18)

        info = tk.Frame(c, bg=WHITE)
        info.pack(side="left", pady=15)

        tk.Label(
            info,
            text=booking["equipment"],
            font=(FONT, 13, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f'{booking["date"]}  •  {booking["time"]}',
            font=(FONT, 10),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=3)

        tk.Label(
            c,
            text="● Confirmed",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(side="right", padx=25)


# ---------------- ISSUES PAGE ----------------

def show_issues():

    clear_content()

    section_title(
        content,
        "🚨 Issues",
        "Report and track laboratory equipment problems."
    )

    create_button(
        content,
        "+ Report New Issue",
        report_issue,
        RED
    ).pack(anchor="e", pady=(0, 15))

    issue = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground="#FECACA",
        highlightthickness=1
    )
    issue.pack(fill="x")

    tk.Label(
        issue,
        text="⚠  Power Supply 01",
        font=(FONT, 14, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=20, pady=(18, 5))

    tk.Label(
        issue,
        text="Power supply output is unstable",
        font=(FONT, 10),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w", padx=20)

    bottom = tk.Frame(issue, bg=WHITE)
    bottom.pack(fill="x", padx=20, pady=15)

    tk.Label(
        bottom,
        text="HIGH PRIORITY",
        font=(FONT, 9, "bold"),
        bg=LIGHT_RED,
        fg=RED,
        padx=8,
        pady=4
    ).pack(side="left")

    tk.Label(
        bottom,
        text="Status: Open",
        font=(FONT, 9, "bold"),
        bg=WHITE,
        fg=RED
    ).pack(side="left", padx=15)

    tk.Label(
        bottom,
        text="Reported: 19 Aug 2026",
        font=(FONT, 9),
        bg=WHITE,
        fg=MUTED
    ).pack(side="right")


def report_issue():

    messagebox.showinfo(
        "Report Issue",
        "Issue reporting form will be connected to the database next."
    )


# ---------------- NOTIFICATIONS PAGE ----------------

def show_notifications():

    clear_content()

    section_title(
        content,
        "🔔 Notifications",
        "Important updates from your laboratory."
    )

    for notification in notifications:

        bg_color = LIGHT_RED if notification["priority"] == "High" else LIGHT_BLUE

        c = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        c.pack(fill="x", pady=6)

        tk.Label(
            c,
            text="●",
            font=(FONT, 15),
            bg=WHITE,
            fg=RED if notification["priority"] == "High" else BLUE
        ).pack(side="left", padx=20)

        info = tk.Frame(c, bg=WHITE)
        info.pack(side="left", pady=15)

        tk.Label(
            info,
            text=notification["title"],
            font=(FONT, 11, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            info,
            text=notification["message"],
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=3)


# ---------------- AI PAGE ----------------

def show_ai():

    clear_content()

    tk.Label(
        content,
        text="🤖 Lab AI",
        font=(FONT, 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Your intelligent laboratory assistant",
        font=(FONT, 11),
        bg=BG,
        fg=MUTED
    ).pack(anchor="w", pady=(2, 20))

    chat = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    chat.pack(fill="both", expand=True)

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
    messages.pack(fill="both", expand=True)

    messages.insert(
        "end",
        "🤖 Lab AI\n\n"
        "Hello! I'm your SmartLab assistant.\n\n"
        "I can help you with:\n"
        "• Equipment availability\n"
        "• Bookings\n"
        "• Maintenance alerts\n"
        "• Equipment health\n"
        "• Reported issues\n"
        "• Laboratory recommendations\n\n"
        "Try asking:\n"
        "\"Which equipment is available?\"\n"
        "\"Which equipment needs maintenance?\"\n"
        "\"Which equipment has the lowest health score?\"\n"
    )

    messages.config(state="disabled")

    bottom = tk.Frame(chat, bg=WHITE)
    bottom.pack(fill="x", padx=20, pady=20)

    entry = tk.Entry(
        bottom,
        font=(FONT, 11),
        bg="#F8FAFC",
        relief="solid",
        bd=1
    )
    entry.pack(side="left", fill="x", expand=True, ipady=10)

    def ask_ai():

        question = entry.get().strip()

        if not question:
            return

        messages.config(state="normal")

        messages.insert(
            "end",
            f"\n\nYou: {question}\n"
        )

        q = question.lower()

        if "available" in q:
            answer = (
                "I found 3 available pieces of equipment: "
                "Oscilloscope 01, Function Generator 01, "
                "and Digital Multimeter 01."
            )

        elif "maintenance" in q or "health" in q:
            answer = (
                "Power Supply 01 currently has the lowest "
                "health score at 63% and is under maintenance."
            )

        elif "book" in q:
            answer = (
                "Oscilloscope 01 is currently available and "
                "has a health score of 94%. I recommend it."
            )

        elif "issue" in q or "problem" in q:
            answer = (
                "There is currently one open issue: "
                "Power Supply 01 has an unstable output."
            )

        else:
            answer = (
                "I can help you with equipment, bookings, "
                "maintenance, issues and laboratory recommendations."
            )

        messages.insert(
            "end",
            f"🤖 AI: {answer}"
        )

        messages.config(state="disabled")
        entry.delete(0, "end")

    create_button(
        bottom,
        "Ask AI",
        ask_ai,
        PURPLE
    ).pack(side="left", padx=10)

    entry.bind("<Return>", lambda event: ask_ai())


# ---------------- SIDEBAR ----------------

sidebar = tk.Frame(root, bg=NAVY, width=245)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Logo

logo = tk.Frame(sidebar, bg=NAVY)
logo.pack(fill="x", padx=25, pady=28)

tk.Label(
    logo,
    text="🧪",
    font=(FONT, 25),
    bg=NAVY,
    fg=WHITE
).pack(side="left")

tk.Label(
    logo,
    text="SmartLab",
    font=(FONT, 20, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(side="left", padx=8)

tk.Label(
    sidebar,
    text="AI-POWERED LAB MANAGEMENT",
    font=(FONT, 8, "bold"),
    bg=NAVY,
    fg="#93C5FD"
).pack(anchor="w", padx=28, pady=(0, 25))


def nav_button(text, command):

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

    button.pack(fill="x", padx=10, pady=2)

    return button


nav_button("🏠   Dashboard", show_dashboard)
nav_button("🔬   Equipment", show_equipment)
nav_button("📅   Bookings", show_bookings)
nav_button("🚨   Issues", show_issues)
nav_button("🔔   Notifications", show_notifications)
nav_button("🤖   Lab AI", show_ai)

# Bottom profile

profile = tk.Frame(sidebar, bg="#1E3A8A")
profile.pack(side="bottom", fill="x", padx=12, pady=15)

tk.Label(
    profile,
    text="AR",
    font=(FONT, 12, "bold"),
    bg=BLUE,
    fg=WHITE,
    width=3,
    height=1
).pack(side="left", padx=12, pady=12)

profile_info = tk.Frame(profile, bg="#1E3A8A")
profile_info.pack(side="left", pady=10)

tk.Label(
    profile_info,
    text="Arun Kumar",
    font=(FONT, 9, "bold"),
    bg="#1E3A8A",
    fg=WHITE
).pack(anchor="w")

tk.Label(
    profile_info,
    text="Student",
    font=(FONT, 8),
    bg="#1E3A8A",
    fg="#BFDBFE"
).pack(anchor="w")


# ---------------- MAIN CONTENT ----------------

main = tk.Frame(root, bg=BG)
main.pack(side="right", fill="both", expand=True)

# Header

header = tk.Frame(
    main,
    bg=WHITE,
    height=70,
    highlightbackground=BORDER,
    highlightthickness=1
)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="SMARTLAB AI",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(side="left", padx=30)

tk.Label(
    header,
    text="● Lab Online",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=GREEN
).pack(side="right", padx=30)

# Content area

content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True, padx=35, pady=30)

# Start on dashboard

show_dashboard()

root.mainloop()