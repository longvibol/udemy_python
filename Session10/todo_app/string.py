def prepare(text):
    text = text.title()
    text = text.strip()
    return text


print(prepare("hello    "))