import os

# Get current working directory
cwd = os.getcwd()
print("Current working directory:", cwd)

# List all files and directories
items = os.listdir(cwd)
print("Files and directories:", items)