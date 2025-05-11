import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from optimum.bettertransformer import BetterTransformer

import speech_recognition as sr
import time

def record_audio(record_seconds=5, silence_threshold=1000):
    r = sr.Recognizer()
    recorded_audio = None

    with sr.Microphone(device_index=2) as source:
        print("Speak now...")
        audio = r.listen(source, timeout=record_seconds)

    if audio:
        try:
            energy = r.energy_threshold 
            start_time = time.time()
            silence_started = False

            for chunk in audio.get_wav_chunks():
                rms = sr.rms(chunk) 
                if rms < energy: 
                    silence_started = True
                if silence_started and (time.time() - start_time) * 1000 > silence_threshold:
                    break

            if not silence_started:
                return audio.get_wav_data()
            else:
                return 0
        except Exception as e:
            print("Error:", e)

def transcribe_with_whisper(audio_data):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "distil-whisper/distil-medium.en"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    model = model.to_bettertransformer()
    processor = AutoProcessor.from_pretrained(model_id)

    transcribe_pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=15,  # Long form transcription
        batch_size=16,
        torch_dtype=torch_dtype,
        device=device,
    )

    text = transcribe_pipe(audio_data)["text"]
    return text

print("done")



if __name__ == '__main__':
    while True:
        Audio = record_audio()
