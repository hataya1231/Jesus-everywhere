import ollama
text = input("User:")
response = ollama.chat(
    model="gemma3:1b",
    messages=[{'role': 'user', 'content': f"あなたはキリスト教祖です。カッコの中の文章に対して相応の返事をしてください。「{text}」また必ず語り口調で答えてください",}],
    stream=True, # ストリーミングを有効化
)

# チャンクごとに順次出力する
for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
