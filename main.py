import webbrowser
import openai
import pyttsx3
import speech_recognition as sr
import os
import datetime

from config import apikey

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Adnan: {query}\n Flash: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text =f"Openai response from prompt: {prompt}\n *****************\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "prompt"
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    engine = pyttsx3.init()  # Initialize the text-to-speech engine
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait for the speech to finish


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            # print("Recognizing...")
            query = r.recognize_google(audio, language="en-us")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "some error occured"


if __name__ == '__main__':
    print('PyCharm')
    say("Hello I am Flash AI, How may i assist you")
    while True:
        print("Listening....")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"],
                 ["Udemy", "https://udemy.com"],
                 ["Chat GPT", "https://chat.openai.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"opening {site[0]} sir")
                webbrowser.open(site[1])
        if "open music".lower() in query:
            musicPath = r"C:\Users\admin\Downloads\Suzume.mp3"
            os.system(f'start "" "{musicPath}"')
        if "the time".lower() in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"sir the time is {strfTime}")
        apps = [["docker desktop", r"C:\Users\admin\Desktop\Docker Desktop.lnk"],
                ["Visual Studio Code", r"C:\Users\admin\Desktop\Visual Studio Code.lnk"],
                ["Google Chrome", r"C:\Users\Public\Desktop\Google Chrome.lnk"]]
        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                say(f"opening {app[0]} sir")
                # desktopShortcut = r"C:\Users\admin\Desktop\Docker Desktop.lnk"
                os.system(f'start "" "{app[1]}"')

        if "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        if "Jarvis Quit".lower() in query.lower():
            exit()

        if "reset chat".lower() in query.lower():
            chatStr = ""

else:
    print("Chatting...")
    chat(query)
