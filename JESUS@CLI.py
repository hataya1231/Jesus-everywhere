from ollama import chat
while True:
    text = input("User:")

    response = chat(model='gemma3:270m', messages=[
    {
        'role': 'user',
        'content': f"Jesus:{text}",
    },
    ])
    print(response.message.content)