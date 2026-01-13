import re
pattern = re.compile("[a-zA-Z ,]+\n\n")
findings = re.findall(pattern, book)
findings = [item.strip("\n\n") for item in findings]
findings