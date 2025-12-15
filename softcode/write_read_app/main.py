contents =["All carrots are to be sliced long",
           "The long live living",
           "Hello Student from Python"]
filenames=["doc.txt","report.txt","presentation.txt"]

for content, filename in zip(contents, filenames):
    file = open(f"./files/{filename}","w")
    file.write(content)

