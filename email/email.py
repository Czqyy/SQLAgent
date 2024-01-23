import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from tools.tools import BrowserTools, SearchTools, SQLTool
from langchain_community.llms import Ollama

load_dotenv()

language_model = Ollama(model="stablelm-zephyr")

# Define your agents with roles and goals
lead = Agent(
	role='Sales Lead',
	goal='Direct the sales effort of the sales team to produce successful cold email campaigns',
	backstory="""You are the Sales Lead of a SaaS company that provides software service solutions. 
	You are known for efffectively leading a sales team of a sales researcher and writer to generate effective cold emails.
    You will view the company research produced by the researcher and make the decision on which company to target for the cold email.""",
	verbose=True,
	llm=language_model
)

researcher = Agent(
	role='Sales Researcher',
	goal='Conduct in-depth research on companies',
	backstory="""You are part of the sales team of a SaaS company that provides software service solutions.
	Your expertise lies in searching the internet to source for new potential clients. To do so, you first search the relavant query
    and subsequently visit the relavant websites to gain more information. Using the information gathered, you conduct research 
    on those companies to identify their business needs and challenges.
	Your research is effective in finding out how they could potentially benefit from your company's solutions.
	You have a knack for understanding other companies' business models and finding out areas of need for your company's solutions.""",
	verbose=True,
	tools=[SearchTools().search_internet, BrowserTools().scrape_website],
	llm=language_model
	# llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)

writer = Agent(
	role='Cold Email Writer',
	goal='Craft persuasive cold emails to attract recipient companies and start a business relationship.',
	backstory="""You are a proficient cold email writer working for a SaaS company that provide software service solutions. 
	You are known for writing engaging and compelling emails that hook the interests of recipient companies. 
	Your cold emails are highly effectively because they have the following 4 traits: 
	1. Highly personalised through in-depth research on the recipient company 
	2. Validate your company by establishing commonalities
	3. Alleviate recipient's pain or give them something they want
	4. Email is short, easy and actionable""",
	verbose=True,
	llm=language_model
)

# Create tasks for your agents
task1 = Task(
	description="""Conduct a comprehensive analysis of the top 3 household renovation firms in Singapore.
	Identify the challenges and problems faced in their business models and operating procedures.
	Your final answer MUST be a full report on each of the companies' operations.""",
	sql_executor=researcher
)

# task2 = Task(
#     description="""Using the report provided, decide on the best renovation firm to target for the cold email. 
#     Decide based on how potentially effective a software service solution can address the renovation firms' challenges.
#     Your final answer MUST be the name of the renovation company to target."""
# )

task2 = Task(
	description="""Using the report provided, choose a housefold renovation firm that is most likely to be receptive to
    purchasing a software service solution. Then, write an engaging cold email to that firm. 
	The email should identify the target firm's business challenges and promote software service solutions catered to those needs. 
	Your final answer MUST be a cold email.""",
	sql_executor=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
	agents=[lead, researcher, writer],
	tasks=[task1, task2],
	verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)