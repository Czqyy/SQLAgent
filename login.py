import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew



def authenticate(agent, username, password):
    start = time.time()

    task = Task(
        description=f"""Username: {username}, password: {password}
        Authenticate these login credentials.""",
        agent=agent
    )

    # crew.tasks.append(task)

    # Get your crew to work!
    # result = crew.kickoff()
    result = task.execute()
    end = time.time()
    print(f"Process took {end - start}s")
    response = {
        "status": 200,
        "message": result
    }
    return response