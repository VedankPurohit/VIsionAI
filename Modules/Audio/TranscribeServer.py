import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" #Temp workaround

from flask import Flask, jsonify
from faster_whisper import WhisperModel
import torch

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

model_size = "distil-medium.en"
model = WhisperModel(model_size, device=device, compute_type="float16")

def Transcribe():
    try:
        segments, info = model.transcribe(audio="audio.wav", beam_size=5, 
            language="en", max_new_tokens=128, condition_on_previous_text=False)
        segments = list(segments)
        extracted_texts = [segment.text for segment in segments]
        extracted_texts = "".join(extracted_texts)
        return extracted_texts
    except Exception as e:
        print("Transcription Error:", e)
        return ""

app = Flask(__name__)

@app.route('/transcribe', methods=['GET'])
def transcribe_audio():
    result = Transcribe()
    return jsonify({'transcription': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
