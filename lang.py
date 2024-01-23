from langchain.agents import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import Ollama

# from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit

db = SQLDatabase.from_uri("mysql://root:password@localhost:3306/command_centerdb")

language_model = Ollama(model="stablelm-zephyr")

agent_executor = create_sql_agent(
    llm=language_model,
    toolkit=SQLDatabaseToolkit(db=db, llm=language_model),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run(
    "List the all the users in the aspnetusers table?"
)