

import customtkinter as ctk
from ollama import chat
from ollama import ChatResponse
from PIL import Image
import threading
import json
from pathlib import Path
from settings import prompt
import random

def UserInsertText(text):
    textbox.insert("end",f"you:{text}\n")
    textbox.see("end")
    textbox.update()

def AiInsertText(text):
    global n
    global flag
    count = 0

    stream = chat(
        model='gemma3:1b',
        messages=chatHistory(text,"userText"),
        stream=True,
    )


    response_text = ""
    for chunk in stream:
        count += 1 
        content =chunk['message']['content']
        if flag == True:
            textbox.insert("end","Jesus:")
            flag = False
        textbox.insert("end",content)
        textbox.see("end")
        app.update()
        if count % 4 == 0:
            n = changeImage(n)
        response_text = response_text + content
    textbox.insert("end","\n")
    chatHistory(response_text)
    button.configure(state = "normal")
    entry.configure(state ="normal")

def sendMessage(event = None):
    global flag
    text = entry.get().strip()
    if text == "":
        return
    button.configure(state = "disabled")
    entry.configure(state = "disabled")
    UserInsertText(text)
    flag = True
    AiInsertText(text)
    entry.delete(0,"end") #入力欄のデータ削除

def creatThread(event = None):
    thread1 = threading.Thread(target = sendMessage)
    thread1.start()

def chatHistory(text,which =None):
    if which == "userText":
        history.append({
            "role":"user",
            "content":text
        })
    else:
        history.append({
            "role":"assistant",
            "content":text
        })
    print(history)
    return history

def saveHistory(new_history,f):
    with open("./memory.json","w") as f:
        json.dump(new_history,f,indent = 2)

"""
def changeImage(m,x):
    if x == 0:
        print(x)
        ran = int(random.randint(0,1))
        print(f"{ran}ランダム")
        image_list[ran].grid(row = 0,column = 0)
        m = ran
        return m
    return m
"""
def changeImage(now_index):
    global jesus_label,image_objects
    if now_index == 0:
        jesus_label.configure(image=image_objects[1])
        return 1
    else:
        jesus_label.configure(image=image_objects[0])
        return 0
        
file_path = Path("./memory.json")
if file_path.exists() == False:
    print("creat a new memory")
    system = [{"role":"system","content":prompt}]
    with open("memory.json","w") as f:
        json.dump(system,f,indent =2)
    history = system
else:
        with open("memory.json","r",encoding = "UTF=8") as f:
            history = json.load(f)

try:
    ctk.set_appearance_mode("dark") #ダークモード
    app = ctk.CTk() #ウィンドウの起動
    app.geometry("800x400") #ウィンドウの大きさ(横*縦)
    app.title("JESUS") #タイトル
    app.grid_columnconfigure(0,weight=1) #0列目の列の長さをウィンドウに合わせて伸ばす
    app.grid_rowconfigure(1,weight=1) #1行目の行の長さをウィンドウに合わせて伸ばす


    #画像出力
    n = 0
    image_objects = []
    img1 = Image.open("./images/jesus-close.png")
    img2 = Image.open("./images/jesus-open.png")
    for img in [img1,img2]:
        resized_img = img.resize(
            (256,256),
            Image.NEAREST
        )

        ctk_img = ctk.CTkImage(
            light_image=resized_img,
            dark_image=resized_img,
            size=(256,256)
        )
        image_objects.append(ctk_img)

    jesus_label = ctk.CTkLabel(
        app,
        image = image_objects[0],
        text = ""
    )
    jesus_label.grid(row = 0,column = 0)

    #テキストボックス
    textbox = ctk.CTkTextbox(app)
    textbox.grid(row = 1,column = 0,columnspan = 2,sticky ="nsew")

    #入力欄
    entry = ctk.CTkEntry(app)
    entry.grid(row = 2,column = 0,sticky = "ew")
    entry.bind("<Return>",creatThread)

    #ボタン
    button = ctk.CTkButton(
        app,
        text = "Push",
        command = creatThread
        )
    button.grid(row = 2,column = 1) #ボタンの設置

    app.mainloop()
finally:
        with open("./memory.json") as f:
            saveHistory(history,f)