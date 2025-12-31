import requests

api_key = "00d73fe42a6145498e2dd76c19732e8f"
url=("https://newsapi.org/v2/everything?q=tesla&from=2025-11-30&sortBy=publishedAt&apiKey="
     "00d73fe42a6145498e2dd76c19732e8f")

# Make request
request =requests.get(url)

#Get a dictionary with data
content=request.json()


#Access the article title and description
for article in content["articles"]:
     print(article["title"])
     print(article["description"])
