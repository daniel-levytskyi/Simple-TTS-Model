import pyttsx3
import pyaudio
import vosk
import json
import threading
import sys
import time

#all of the modules
benjamin_active = False
engine = pyttsx3.init()
model = vosk.Model(r"/home/levytskyi/Documents/Python/TTS/Libraries/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 16000, input = True, frames_per_buffer = 8192)

#action list
task_list = []

keywords = {
    "benjamin": "Yes my sire? At your humble service.",
    "weather": "Do you really think that I am that smart? Go check it on your phone's weather app, genius.",
    "time": "Don't ask me that ever again. You literally have it in the bottom right of your screen. Better yet, take out your phone and look at the time there you all-knowing genius.",
    "calculations": "calculations",
    "list": "list",
    "alarm": "alarm",
}

#definitions



#TIMER
timer_remaining = "No alarm active."
def countdown(t):
    global timer_remaining
    while t:
        mins, secs  = divmod(t, 60)
        timer_remaining = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1
        if t == 0:
            timer_remaining = "Time's Up!"
            break
def start_timer(duration):
    timer_thread = threading.Thread(target = countdown, args=(duration,))
    timer_thread.start()
def get_timer_data():
    engine.say("Initializing your alarm program, my lord")
    engine.runAndWait()
    engine.say("Loading completed. How many minutes would you like to set your alarm for sir?")
    engine.runAndWait()
    minutes = int(input("Enter amount: "))
    engine.say("Starting up your timer sir.")
    engine.runAndWait()
    start_timer(minutes * 60)
    print("Listening...")



#TO DO LIST
def active_list():
    engine.say("Inintializing your to do list, my lord")
    engine.runAndWait()
    while True:
        print("==========To do list==========")
        print("1. Add a task")
        print("2. Complete a task")
        print("3. View all tasks")
        print("4. Quit program")
        chosen_option = input("Choose a number to perform: ")
        if chosen_option not in ["1", "2", "3", "4"]:
            print_error_message()
        elif chosen_option == "1":
            add_task()
        elif chosen_option == "2":
            complete_task()   
        elif chosen_option == "3":
            view_tasks()
        elif chosen_option == "4":
            print("change da world my final message. Goodb ye")
            engine.say("change da world my final message. Goodb ye")
            engine.runAndWait()
            print("Listening...")
            break
def print_error_message():
    print("Please input an option by its number (1, 2, 3, 4): ")
    engine.say("Please input an option by its number sir")
def add_task():
    engine.say("What task would you like to add sir?")
    engine.runAndWait()
    add = input("What task would you like to add?: ")
    task_list.append(add)
    print("Task added successfully.")
    engine.say("Task added successfully")
    engine.runAndWait()
def complete_task(): 
    engine.say("Here are your tasks sir")
    engine.runAndWait()
    print("Here are your tasks: ")
    print("\n".join(task_list))
    engine.say("What task would you like to complete sir?")
    engine.runAndWait()
    completed = input("What task would you like to complete?: ")
    if completed in task_list:
        task_list.remove(completed)
        print("Task successfully completed")
        engine.say("Task successfully completed sir")
        engine.runAndWait()
    else:
        engine.say("Sorry sir, that task was not found")
        engine.runAndWait()        
def view_tasks():
    engine.say("Here are your tasks sir")
    engine.runAndWait()
    print("Here are your tasks: ")
    print("\n".join(task_list))



#CALCULATOR
def calculations():
    engine.say("What is the first number for calculation, my sire?")
    engine.runAndWait()
    num_1 = int(input("Input first number here: "))
    engine.say("What operation would you like to perform?")
    engine.runAndWait()
    user_input_operation = input("Input operation here (+,-,*,/): ")
    engine.say("What is the second number for calculation?")
    engine.runAndWait()
    num_2 = int(input("Input second number here: "))

    if user_input_operation == "+":
        engine.say("Here is your result, my lord")
        engine.runAndWait()
        print("Result: " + str(num_1 + num_2))
    elif user_input_operation == "-":
        engine.say("Here is your result, my lord")
        engine.runAndWait()
        print("Result: " + str(num_1 - num_2))
    elif user_input_operation == "*":
        engine.say("Here is your result, my lord")
        engine.runAndWait()
        print("Result: " + str(num_1 * num_2))
    elif user_input_operation == "/":
        engine.say("Here is your result, my lord")
        engine.runAndWait()
        print("Result: " + str(num_1 / num_2))

def termination():  
    quit()

#running whatever function is in the action list
def perform_action(action_text):
    if keyword == "alarm":
        get_timer_data()
        while True:
            print(f"\r{timer_remaining}", end = '', flush = True)
    elif keyword == "calculations":
        calculations()
    elif keyword == "list":
        active_list()
    else:
        print("Benjamin said: " + action_text)
        engine.say(action_text)
        engine.runAndWait()
        print("Listening...")

#starting up the audio input
stream.start_stream()
print("Listening...")

#langauge processing and outputs
while True:
    data = stream.read(8192)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")
        #if statement added for debug, will be removed later
        if text:
            print(text)
        for keyword, action_text in keywords.items():
            if "termination" in text:
                print("Program terminated. Shutting down all non-essential tasks.")
                sys.exit()
            if "benjamin" in text:
                benjamin_active = True
                perform_action(action_text)
                break
            if keyword in text and benjamin_active == True:
                perform_action(action_text)
                break

#closing and stopping everything
