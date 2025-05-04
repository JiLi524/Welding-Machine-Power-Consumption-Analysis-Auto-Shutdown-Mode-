import random
from datetime import datetime, timedelta
import pandas as pd


def simulate_welding_records(num_records=100, interval_seconds=10, start_date=None):
    """
    This script simulates the operation records of a welding machine. Each record includes:
    - timestamp: the exact time of the record
    - state: running, idle or shutdown
    - power: Power consumption (high when running; low or zero when idle or shutdown)
    - auto_shutdown: True if continuously idle for more than 180 seconds, else False

    Parameters:
    - num_records: Number of records to generate
    - interval_seconds: Time interval between consecutive records (in seconds)
    - start_date: the starting time, either as a string "YYYY-MM-DD HH:MM:SS" or a datetime object; defaults to the current time if None
    """
    # Define the list of possible states (not directly used here but kept for future expansion)
    states = ["running", "idle", "shutdown"]

    # Initialize the starting state as 'running' and set up idle time tracking
    current_state = "running"
    idle_duration = 0

    # Set the starting timestamp
    if start_date is None:
        current_time = datetime.now()
    else:
        if isinstance(start_date, str):
            try:
                current_time = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("start_date 格式错误，请使用 'YYYY-MM-DD HH:MM:SS'")
        elif isinstance(start_date, datetime):
            current_time = start_date
        else:
            raise TypeError("start_date 必须为字符串或 datetime 对象")

    records = []

    for i in range(num_records):
        # Accumulate idle_duration when in 'idle' state; reset if in any other state
        if current_state == "idle":
            idle_duration += interval_seconds
        else:
            idle_duration = 0

        # Determine power and auto_shutdown based on the current state
        if current_state == "running":
            power = round(random.uniform(500, 1500), 2)
            auto_shutdown = False
        elif current_state == "idle":
            power = round(random.uniform(80, 100), 2)
            auto_shutdown = idle_duration >= 180  # idle 累计超过 180 秒则置 True
        elif current_state == "shutdown":
            power = 0
            auto_shutdown = False

        # Record the current state data
        record = {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "state": current_state,
            "power": power,
            "auto_shutdown": auto_shutdown
        }
        records.append(record)

        # Update the timestamp
        current_time += timedelta(seconds=interval_seconds)

       # State transitions ensuring continuity: usually maintain the current state, occasionally switch
        if current_state == "running":
            current_state = random.choices(
                population=["running", "idle", "shutdown"],
                weights=[0.9, 0.05, 0.05],
                k=1
            )[0]
        elif current_state == "idle":
            current_state = random.choices(
                population=["idle", "running", "shutdown"],
                weights=[0.92, 0.04, 0.04],
                k=1
            )[0]
        elif current_state == "shutdown":
            current_state = random.choices(
                population=["shutdown", "idle", "running"],
                weights=[0.80, 0, 0.2],
                k=1
            )[0]

    return records


if __name__ == "__main__":
    start_date = "2025-05-03"
    start_time = "08:00:00"
    start = start_date + " " + start_time
    data = simulate_welding_records(num_records=7500, interval_seconds=5, start_date=start)

    df = pd.DataFrame(data)
    df.to_csv(f"{start_date}-welding_machine_records.csv", index=False, encoding="utf-8-sig")
