from ollama import chat
while True:
    text = input("User:")

    response = chat(model='gemma3:1b', messages=[
    {
        'role': 'user',
        'content': f"あなたはキリスト教祖です。カッコの中の文章に対して相応の返事をしてください。「{text}」また必ず語り口調で答えてください",
    },
    ])
    print(f"Jesus:{response.message.content}")