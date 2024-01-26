from flask import Flask, render_template, request, jsonify
from login import authenticate
from dotenv import load_dotenv
from crewai import Agent, Crew
from tools.tools import SQLTool


app = Flask(__name__)

load_dotenv()

login_handler = Agent(
    role='Login Authenticator',
    goal='Authenticate login request for given username and password',
    backstory=f"""Given login credentials, query the 'users' table in the MySQL database to compare the credentials.
        If the query result is empty, IMMEDIATELY return 'UNSUCCESSFUL'.
        Else, return 'SUCESS'.
        Do so in the fastest possible way.""",
    allow_delegation=True,
    tools=[SQLTool().query],
    verbose=True
)

# Instantiate your crew with a sequential process
# crew = Crew(
#     agents=[login_handler],
#     tasks=[],
#     verbose=2, # You can set it to 1 or 2 to different logging levels
# )



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with actual API call
        api_response = authenticate(login_handler, username, password)
        # crew.tasks.pop(0)

        return render_template('login.html', api_response=api_response)

    return render_template('login.html', api_response=None)


if __name__ == '__main__':
    app.run(debug=True)
