import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew



def authenticate(agent, username, password):
    task = Task(
        description=f"""Username: {username}, password: {password}
        Authenticate these login credentials.""",
        agent=agent
    )

    # crew.tasks.append(task)

    # Get your crew to work!
    # result = crew.kickoff()
    start = time.time()
    print("STARTING TASK")
    result = task.execute()
    end = time.time()
    print(f"END TASK: {end - start}s")
    response = {
        "status": 200,
        "message": result
    }
    return response