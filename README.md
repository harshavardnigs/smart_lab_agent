# smart lab agent:

## Problem Statement

Managing a lab involves keeping track of equipment, bookings, maintenance, and issues. When this information is stored separately or has to be checked manually, it can be difficult to know what equipment is available, what needs maintenance, or what problems need attention. Our project aims to bring this information together in one system.

## Solution

Smart Lab Operations Agent is a lab management application built using Python. It allows users to view equipment, check its availability and health, make bookings, report issues, and view notifications.

The application has a frontend built with Tkinter and a FastAPI backend. The backend connects to Exasol Personal using PyExasol, where the lab data is stored.

The project also includes a Lab AI interface and a dashboard insight based on equipment health data. The Lab AI interface is currently prepared for future AI model integration.

## How Exasol Personal is Used

Exasol Personal is used as the primary data platform for the project.

The `SMARTLAB` schema stores information related to:

- Users
- Equipment
- Bookings
- Usage history
- Issues
- Notifications

The FastAPI backend connects to Exasol using PyExasol.

When the application needs to display equipment, booking, issue, or notification information, the backend retrieves it from Exasol. Similarly, when a user creates a booking or reports an issue, the information is stored in the Exasol database.

For example:

- Equipment details are read from the `EQUIPMENT` table.
- New bookings are added to the `BOOKINGS` table.
- Equipment availability is updated after a booking.
- Reported problems are stored in the `ISSUES` table.
- Notifications are stored and retrieved from the `NOTIFICATIONS` table.

## Features

## Features

- View and search lab equipment with availability, health, and maintenance details
- Book equipment and view existing bookings
- Report equipment issues with priority tracking
- View and manage notifications for lab updates and reported issues
- Monitor lab activity through the dashboard with equipment health insights
- Lab AI interface prepared for future AI model integration
  
## Project Structure

smart_lab_agent
├── backend.py
├── frontend.py
├── database.sql
├── load_to_exasol.py
├── pyproject.toml
├── uv.lock
├── .python-version
└── src/
    └── smart_lab_agent/
        └── __init__.py
