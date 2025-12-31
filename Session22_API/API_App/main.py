from operator import index

import requests
from send_email import send_email

api_key = "00d73fe42a6145498e2dd76c19732e8f"
url=("https://newsapi.org/v2/everything?q=tesla&from=2025-11-30&sortBy=publishedAt&apiKey="
     "00d73fe42a6145498e2dd76c19732e8f")

# Make request
request =requests.get(url)

#Get a dictionary with data
content=request.json()


#Access the article title and description
body = ""
for article in content["articles"]:
     if article["title"] and article["description"] is not None:
          body = body + article["title"] +":"+ "\n" + article["description"] + 2*"\n"

body = body.encode('utf-8')
send_email(body)

body = body.decode('utf-8')
print(body)