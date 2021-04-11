import voice_assistant as va


def main():
    va.VoiceAssistant(
        micro_index=2,
        timeout=5,
        language="en-US",
        print_response=True,
        speak_response=True,
        pre_message="Meow meow",
        pardon_message="Pardon me, please say that again",
        start_message="Hello, human, I am a simple voice assistant"
    ).loop(end_condition=True, can_restart=True)


if __name__ == '__main__':
    main()
