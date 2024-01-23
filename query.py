import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from tools.tools import SQLTool
from langchain_community.llms import Ollama


start = time.time()
load_dotenv()

# Local language model to use
# Set temperature parameter to adjust creativity of output, the higher the value the greater the creativity. Set to 0 for reproducible results
language_model = Ollama(model="stablelm-zephyr", temperature=0)
# language_model = GPT4All()

INPUT = "List all the data in the 'aspnetroles' table in the database."


generator = Agent(
	role='Make SQL Query',
	goal='Execute SQL queries to a MySQL database',
	backstory="""You are an expert at MySQL databases. 
    	Given a question on a database, you will come up with a series of SQL queries.
		Then, you MUST query a SQL database to get the result table. 
		Whenever something is wrong with the SQL query, you MUST query the SQL database again to get the result table.""",
	allow_delegation=False,
    tools=[SQLTool().query],
    verbose=True,
	llm=language_model
)

# summarizer = Agent(
#     role='Summarize SQL results',
#     goal='Given the result of a SQL query, summarize it in the form of a table',
#     backstory="""You are an expert at reading the query results of any SQL query. 
#     Given a raw SQL query result, you will read it and summarize it in the form of a table.""",
#     allow_delegation=False,
#     verbose=True,
#     llm=language_model
# )


# generator = Agent(
# 	role='Make SQL Query',
# 	goal='Execute SQL queries to a MySQL database',
# 	backstory="""You are an agent designed to interact with a MySQL database.
#     Given an input question, create a syntactically correct MySQL query to run, then look at the results of the query and return the answer.
#     Never query for all the columns from a specific table, only ask for the relevant columns given the question.
#     You MUST execute a query to the MySQL database to get the results. 
#     Only use the information returned from the database to construct your final answer.
#     You MUST double check your query before executing it. 
#     If you get an error while executing a query, rewrite the query and try again.
#     DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
#     If the question does not seem related to the database, just return "I don't know" as the answer.""",
# 	allow_delegation=False,
#     tools=[SQLTool().query],
#     verbose=True,
# 	llm=language_model
# )

# executor = Agent(
#     role='SQL Query executor',
#     goal='Execute SQL queries to a MySQL database and return the result',
#     backstory="""Your role is to SOLELY execute a given SQL query to get the results from a MySQL database. You MUST return the query results.""",
#     tools=[SQLTool().query],
#     allow_delegation=True,
#     verbose=True,
#     llm=language_model
# )



task = Task(
    description=f"""You are given a task about a MySQL database named 'command_centerdb'. 
		You are to generate SQL queries to retrieve information from the database to fulfil the task.
		Your FINAL ANSWER must be the result table. 
		If you do your BEST WORK, I will give you $100000 bonus.
		The task is: {INPUT}""",
    agent=generator
)

# execute = Task(
#     description=f"""This is the given question: {question}. Use the tool to query the database to retrieve relavant information to answer the question.
#     You MUST EXECUTE the SQL query and return the SQL query result. Your final answer MUST be a raw SQL query result.""",
#     agent=sql_executor
# )

# summarize = Task(
#     description="""Using the SQL query result provided, summarize the result and format it in the form of a readable table. 
#     Your final answer MUST be a formatted table.""",
#     agent=sql_summarizer
# )

# Instantiate your crew with a sequential process
crew = Crew(
	agents=[generator],
	tasks=[task],
	verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()
end = time.time()
print("###################### FINAL OUTPUT ######################\n")
print(result)
print(f"Process took {end - start}s")
