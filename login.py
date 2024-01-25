import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from tools.tools import SQLTool


username = ""
password = ""

start = time.time()
load_dotenv()

login_handler = Agent(
    role='Login Authenticator',
    goal='Authenticate login request for given username and password',
    backstory=f"""Given login credentials, query the 'sqlagent' table in the MySQL database to compare the credentials.
        If the credentials match, return 'SUCCESS', else return 'UNSUCCESSFUL'.""",
    allow_delegation=True,
    tools=[SQLTool().query],
    verbose=True
)

# sql_agent = Agent(
# 	role='Make SQL Query',
# 	goal='Query a MySQL database',
# 	backstory="""You are an expert at MySQL relational databases.
# 		The database consists of a table named 'sqlagent'.
#         Query the MySQL database to get table data relavant to the task.""",
# 	allow_delegation=False,
#     tools=[SQLTool().query],
#     verbose=True
# )

task = Task(
    description="""Username: {username}, password: {password}
    Authenticate these login credentials.""",
    agent=login_handler
)

# Instantiate your crew with a sequential process
crew = Crew(
	agents=[login_handler],
	tasks=[task],
	verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()
end = time.time()
print("###################### FINAL OUTPUT ######################\n")
print(result)
print(f"Process took {end - start}s")