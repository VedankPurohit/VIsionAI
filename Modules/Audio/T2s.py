from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

print("Loading TTS model...")
# generate speech by cloning a voice using default settings
tts.tts_to_file(text="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
                file_path=r"Modules\Audio\output.wav",
                speaker_wav=[r"Modules\Audio\test.wav"],
                language="en",
                split_sentences=True
                )

print("Done")