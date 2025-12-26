import os

# Get current working directory
cwd = os.getcwd()
print("Current working directory:", cwd)

# Define new directory path
new_dir = os.path.join(cwd, "test_directory")

# Create the directory
os.mkdir(new_dir)

print("Directory 'test_directory' created successfully!")