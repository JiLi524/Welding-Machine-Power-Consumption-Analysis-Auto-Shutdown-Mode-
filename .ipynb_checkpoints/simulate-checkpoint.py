import random
from datetime import datetime, timedelta
import pandas as pd


def simulate_welding_records(num_records=100, interval_seconds=10, start_date=None):
    """
    模拟生成电焊机状态记录，每条记录包含：
    - timestamp: 时间戳
    - state: running, idle 或 shutdown
    - power: 功率（running时随机生成较大数值，idle和shutdown时较低或为0）
    - auto_shutdown: 如果连续 idle 超过180秒则为 True，否则为 False

    参数：
    - num_records: 生成记录数
    - interval_seconds: 相邻记录的时间间隔（秒）
    - start_date: 起点日期，格式为 "YYYY-MM-DD HH:MM:SS" 的字符串，或 datetime 对象；为 None 时默认当前时间
    """
    # 定义状态列表（此处虽然没有直接使用，但可供后续扩展参考）
    states = ["running", "idle", "shutdown"]

    # 初始化起始状态为 running，并初始化 idle 状态累计时间
    current_state = "running"
    idle_duration = 0

    # 设置起始时间
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
        # 如果当前状态是 idle，则累加 idle_duration，否则重置
        if current_state == "idle":
            idle_duration += interval_seconds
        else:
            idle_duration = 0

        # 根据状态选择功率值和 auto_shutdown 标志
        if current_state == "running":
            power = round(random.uniform(500, 1500), 2)
            auto_shutdown = False
        elif current_state == "idle":
            power = round(random.uniform(80, 100), 2)
            auto_shutdown = idle_duration >= 180  # idle 累计超过 180 秒则置 True
        elif current_state == "shutdown":
            power = 0
            auto_shutdown = False

        # 记录当前状态数据
        record = {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "state": current_state,
            "power": power,
            "auto_shutdown": auto_shutdown
        }
        records.append(record)

        # 更新时间戳
        current_time += timedelta(seconds=interval_seconds)

        # 状态转换，保证一定的连续性：多数情况下保持当前状态，少数情况下切换
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
