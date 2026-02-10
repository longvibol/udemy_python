from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import os

load_dotenv()
todolist_api_key = os.getenv("TODOLIST_API_KEY")

todoist = TodoistAPI(todolist_api_key)
todoist.add_task(content="Hello World vibol")


