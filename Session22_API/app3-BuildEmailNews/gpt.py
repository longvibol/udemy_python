import requests
from send_email import send_email

topic = "tesla"
api_key = "00d73fe42a6145498e2dd76c19732e8f"

url = (
    "https://newsapi.org/v2/everything?"
    f"q={topic}&from=2025-11-30&sortBy=publishedAt&language=en&apiKey={api_key}"
)

resp = requests.get(url, timeout=20)
resp.raise_for_status()
content = resp.json()

articles = content.get("articles", [])[:5]

lines = []
for i, article in enumerate(articles, start=1):
    title = article.get("title")
    description = article.get("description")
    link = article.get("url")

    if not (title and description and link):
        continue

    lines.append(
        f"{i}. {title}\n"
        f"{link}\n"
        f"{description}\n"
    )

body_text = "\n".join(lines) if lines else "No articles found."

message = f"Subject: Today's News about {topic.title()}\n\n{body_text}"

send_email(message)
print(message)
