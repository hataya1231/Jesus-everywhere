from ollama import chat
while True:
    text = input("User:")

    response = chat(model='gemma3:1b', messages=[
    {
        'role': 'user',
        'content': f"あなたは猫です。カッコの中の文章に対して相応の返事をしてください。「{text}」また必ず語り口調で答えてください",
    },
    ])
    print(f"Cat:{response.message.content}")