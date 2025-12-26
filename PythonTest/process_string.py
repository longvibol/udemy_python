def format_filename():
    filename = "report.txt"
    f = filename.split(".txt")[0].capitalize()
    # formatted_name = filename[:-4].capitalize()
    return f

print(format_filename())