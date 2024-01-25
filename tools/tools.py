import os
import json
import requests
from langchain.tools import tool
# from unstructured.partition.html import partition_html
import mysql.connector


class SQLTool():
	@tool("Query MySQL database")
	def query(sql_query):
		"""Useful to execute a given SQL query in a MySQL database and return the query result
		The given SQL query must be in exact MySQL syntax."""
		cnx = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='command_centerdb')
		cursor = cnx.cursor()
		result = ""
		try:
			cursor.execute(sql_query)
			result = cursor.fetchall()
			print("\n###################### QUERY OUTPUT ######################\n")
			print(result)
		except Exception as e:
			print(e)
			result = f"Something is wrong with the SQL query, you got the error {e}"
		finally:
			cnx.close()
			return result


# class BrowserTools():
# 	@tool("Scrape website content")
# 	def scrape_website(website):
# 		"""Useful to scrape a website content"""
# 		url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
# 		payload = json.dumps({"url": website})
# 		headers = {
# 			'cache-control': 'no-cache',
# 			'content-type': 'application/json'
# 		}
# 		response = requests.request("POST", url, headers=headers, data=payload)
# 		elements = partition_html(text=response.text)
# 		content = "\n\n".join([str(el) for el in elements])

# 		# Return only the first 5k characters
# 		return content[:5000]
	
# class SearchTools():
# 	@tool("Search the internet")
# 	def search_internet(query):
# 		"""Useful to search the internet 
# 		about a a given topic and return relevant results"""
# 		top_result_to_return = 4
# 		url = "https://google.serper.dev/search"
# 		payload = json.dumps({"q": query})
# 		headers = {
# 			'X-API-KEY': os.environ['SERPER_API_KEY'],
# 			'content-type': 'application/json'
# 		}
# 		response = requests.request("POST", url, headers=headers, data=payload)
# 		results = response.json()['organic']
# 		string = []
# 		for result in results[:top_result_to_return]:
# 			try:
# 				string.append('\n'.join([
# 					f"Title: {result['title']}", f"Link: {result['link']}",
# 					f"Snippet: {result['snippet']}", "\n-----------------"
# 				]))
# 			except KeyError:
# 				next

# 		return '\n'.join(string)



# print(SQLTool().query("SELECT * FROM command_centerdb.aspnetroles"))		
	