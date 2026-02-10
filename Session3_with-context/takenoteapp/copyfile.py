with open("./journal/story.txt") as file:
    a=(file.read())
    with open("./journal/story_copy.txt",'w') as f:
        f.write(a)