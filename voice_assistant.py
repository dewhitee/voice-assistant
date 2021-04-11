import speech_recognition as sr
import pyttsx3
import datetime
import pyaudio


class VoiceAssistant:

    def __init__(self, micro_index=2, timeout=5, language="en-US", print_response=True,
                 speak_response=False,
                 pre_message="Meow meow",
                 pardon_message="Pardon me, please say that again",
                 start_message="Hello, human, I am a simple voice assistant",
                 stop_words=None,
                 restart_words=None):

        if stop_words is None:
            stop_words = ["goodbye", "good bye", "bye", "stop"]
        if restart_words is None:
            restart_words = ["restart", "wake up"]

        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', 'voices[0].id')

        print(start_message)
        self.speak(start_message)

        self.morning_hello = "Hello, good morning"
        self.afternoon_hello = "Hello, good afternoon"
        self.evening_hello = "Hello, good evening"
        self.shutting_down_message = "Shutting down, good bye"
        self.micro_index = micro_index
        self.timeout = timeout
        self.language = language
        self.print_response = print_response
        self.speak_response = speak_response
        self.pardon_message = pardon_message
        self.pre_message = pre_message
        self.stop_words = stop_words
        self.restart_words = restart_words
        self.start_message = start_message

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak(self.morning_hello)
            print(self.morning_hello)
        elif 12 <= hour < 18:
            self.speak(self.afternoon_hello)
            print(self.afternoon_hello)
        else:
            self.speak(self.evening_hello)
            print(self.evening_hello)

    def take_command(self, print_response, speak_response, timeout, do_pardon):
        r = sr.Recognizer()
        pa = pyaudio.PyAudio()

        with sr.Microphone(device_index=self.micro_index) as source:
            print("Listening...")
            audio = r.listen(source, timeout=timeout)

            try:
                statement = r.recognize_google(audio, language=self.language)
                if print_response:
                    print(f"User said: {statement}\n")
                if speak_response:
                    self.speak(f"User said: {statement}")

            except Exception as e:
                if do_pardon:
                    self.speak(self.pardon_message)
                return "None"

            return statement

    def loop(self, end_condition=True, can_restart=False):
        """
        :param end_condition You can specify custom end condition to break out of the loop.
        :param can_restart Set True if you want to restart voice assistant using the start words. To completely
        shutdown the voice assistant in case this parameter is set to True - you need to say any word from the list
        of the stop_words.
        """
        while end_condition:
            self.speak(self.pre_message)
            statement = self.take_command(
                print_response=self.print_response,
                speak_response=self.speak_response,
                timeout=self.timeout,
                do_pardon=True
            ).lower()

            if statement == 0:
                continue

            if any(w in statement for w in self.stop_words):
                self.speak(self.shutting_down_message)
                print(self.shutting_down_message)
                break

        if can_restart:
            self._waiting_loop(end_condition)

    def _waiting_loop(self, end_condition=True):
        while end_condition:
            statement = self.take_command(
                print_response=False,
                speak_response=False,
                timeout=None,
                do_pardon=False
            ).lower()

            if statement == 0:
                continue

            if any(w in statement for w in self.restart_words):
                print("Restarting!")
                self.speak(self.start_message)
                self.wish_me()
                break

            if any(w in statement for w in self.stop_words):
                self.speak("That's it, bye")
                print("That's it, bye")
                return

        self.loop(end_condition, can_restart=True)
