from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import sqlite3
import os, time

app = FastAPI()

# Создание БД
conn = sqlite3.connect("robot.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS robot_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_number INTEGER,
        start_time TEXT,
        end_time TEXT,
        duration INTEGER
    )
""")
conn.commit()
conn.close()

class RobotParams(BaseModel):
    start_number: int = 0

@app.post("/start_robot/")
def start_robot(params: RobotParams):
    # Запуск робота с числом
    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
    subprocess.Popen(["python", "robot.py", str(params.start_number)])
    return {"message": "Робот запущен"}

@app.post("/stop_robot/")
def stop_robot():
    # Остановка робота
    os.system("taskkill /F /IM python.exe /T")
    return {"message": "Робот остановлен"}

@app.get("/robot_runs/")
def get_robot_runs():
    # Инфа из БД
    conn = sqlite3.connect("robot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM robot_runs")
    runs = cursor.fetchall()
    conn.close()
    return {"robot_runs": runs}
