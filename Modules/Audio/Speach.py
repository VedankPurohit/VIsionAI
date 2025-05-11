import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')

try:
    # Start the microphone and record the audio
    with sr.Microphone(device_index=3) as source:
        print("Please speak now...")
        audio = r.listen(source)

    # Save the audio file
    with open("audio.wav", "wb") as file:
        file.write(audio.get_wav_data())

except Exception as e:
    print("Error:", e)
