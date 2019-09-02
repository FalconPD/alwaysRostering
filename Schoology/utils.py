"""
Basic utilities used by Schoology scripts
"""

import asyncio
import time

async def task_monitor(tasks, interval=30):
    """
    Takes a list of tasks and an update interval and prints a status every
    interval detailing how many tasks were completed
    """
    tasks_completed = 0
    previous_time = time.time()
    for result in asyncio.as_completed(tasks):
        await result
        tasks_completed += 1
        current_time = time.time()
        if (current_time - previous_time) > interval:
            print(f"{tasks_completed} / {len(tasks)} tasks completed")
            previous_time = current_time
