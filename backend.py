from fastapi import FastAPI

app = FastAPI(title="SmartLab AI API")


@app.get("/")
def home():
    return {
        "message": "SmartLab AI API is running!"
    }


@app.get("/equipment")
def get_equipment():
    return {
        "equipment": [
            {
                "id": 1,
                "name": "Oscilloscope 01",
                "availability": "Available",
                "health_score": 94
            },
            {
                "id": 2,
                "name": "Oscilloscope 02",
                "availability": "Booked",
                "health_score": 91
            }
        ]
    }