import requests

urll = "https://c7.alamy.com/comp/2BT1HTF/a-group-of-cute-happy-filipino-children-pose-for-me-in-the-intramuros-old-walled-town-of-manila-the-philippines-2BT1HTF.jpg"

response = requests.get(urll)
response.text

with open("image.jpg", "wb") as file:
    file.write(response.content)