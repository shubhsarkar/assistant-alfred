'''
Please read README.md file to use this assistance properly. All the instructions have been mentioned properly in that file.
'''

import pyttsx3 # Text to Speech.
import datetime 
import speech_recognition as sr # As the name says, it's speech recognition module.
import pyaudio # for audio
import wikipedia
import webbrowser
import os
import re
import pywhatkit as kit # For accessing youtube video
import smtplib # for sending email

''' enter valid email addresses '''
email_dir = {
    'dummy1' : 'dummyemail1@gmail.com',
    'dummy2' : 'dummyemail2@gmail.com',
    'dummy3' : 'dummyemail3@gmail.com'
}

stop = ['alfred stop', 'alfred close', 'close', 'stop']
greetings = ['hi alfred', 'hello alfred', 'hi', 'hello',] 
ask = ['how are you', 'how are you alfred',]

''' Initializing the voices provided by windows '''
engine = pyttsx3.init("sapi5") # For voice API of windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

flag = False
flag2 = False

''' To make the AI speak '''
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

''' To wish me eveytime I run the AI '''
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Master Bruce!")
    elif hour>=12 and hour<5:
        speak("Good Afternoon Master Bruce!")
    else:
        speak("Good Evening Master Bruce!")
    
    speak("I'm your butler Alfred. How may I assist you?")

''' To take command using Speech Recognition. It takes microphone input and returns string output '''
def takeCommand():
    cmd = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        cmd.energy_threshold = 500 # minimum audio energy to consider for recording
        cmd.pause_threshold = 0.8 # seconds of non-speaking audio before a phase is considered complete
        audio = cmd.listen(source)

    try:
        print("Recognizing...")
        query = cmd.recognize_google(audio, language='en-in')
        print("User said:", query)
    except Exception as err:
        return "None"
    return query

''' 
To send an email.
Make sure to replace "your-email@gmail.com" with valid email id and "your-password" 
with your actual password so that the function can access your email id.
For security reasons, you can save your password in a .txt file and read that file using
pandas library.
'''
def sendEmail(emailId):
    speak("What do you wanna say?")
    msg = takeCommand()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    server.sendmail('your-email@gmail.com', emailId, msg)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        flag = False
        flag2 = True
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Alright.")
            speak("According to wikipedia")
            speak(results)
            flag = True
        
        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
            flag = True

        elif 'open google' in query:
            webbrowser.open("www.google.co.in")
            flag = True
        
        elif 'open stackoverflow' in query:
            webbrowser.open("www.stackoverflow.com")
            flag = True

        elif 'open hackerrank' in query:
            webbrowser.open("www.hackerrank.com")
            flag = True

        elif 'open linkedin' in query:
            webbrowser.open("www.linkedin.com")
            flag = True

        elif 'open internshala' in query:
            webbrowser.open("www.internshala.com")
            flag = True
        
        elif 'open gmail' in query:
            webbrowser.open("www.google.com/gmail/")
            flag = True

        elif 'open github' in query:
            webbrowser.open("www.github.com")
            flag = True

        elif 'play' and 'youtube' in query:
            query = query.replace("play", "")
            query = query.replace("youtube", "")
            kit.playonyt(query)
            flag = True

        elif 'search' and 'google' in query:
            query = query.replace("search", "")
            query = query.replace("google", "")
            kit.search(query)
            flag = True

        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak("Sir, the time is"+time)
            flag = True

        elif query in greetings:
            speak("Hello Master Bruce!")
            flag = True
        
        elif query in ask:
            speak("I'm fine. Thank you for asking!")
            flag = True

        elif "send an email" in query:
            try:
                speak("Whom do you want to send an email Master Bruce?")
                name = takeCommand().lower()
                if name in email_dir.keys():
                    emailId = email_dir[name]
                    sendEmail(emailId)
                    speak("Email sent to "+name+" successfully!")
                else:
                    speak("There's not name as "+name+" in the email directory")
            except Exception as err:
                speak("Sorry email cannot be sent!")
            flag = True

        elif query in stop:
            speak("Okay Master Bruce, have a good day!")
            exit()

        else:
            speak("Sorry this action cannot be performed. Anything else?")
        
        if flag:
            speak("Sir, anything else?")
            flag = False