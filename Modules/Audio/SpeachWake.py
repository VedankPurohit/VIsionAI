import speech_recognition as sr
import warnings, time
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from optimum.bettertransformer import BetterTransformer

# Wake word variables
WakeUpWords1 = "Hey Vison"
WakeUpWords2 = "Hey Jarvis"

r = sr.Recognizer()

ListenForUser = True

source = sr.Microphone()
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)


def transcribe_with_whisper(audio_data):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "distil-whisper/distil-medium.en"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True#, use_flash_attention_2=True
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model = model.to_bettertransformer()
    processor = AutoProcessor.from_pretrained(model_id)

    transcribe_pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=15, #long form transcription
        batch_size=16,
        torch_dtype=torch_dtype,
        device=device,
    )

    text = transcribe_pipe(audio_data)
    return text



def HasUserAsked(audio):
    global ListenForUser
    with open("WakeListen.wav", "wb") as f:
        f.write(audio.get_wav_data())
    result = transcribe_with_whisper('WakeListen.wav')
    text_input = result['text']
    if WakeUpWords1 in text_input.lower().strip() or WakeUpWords2 in text_input.lower().strip():
        print("Ask the Question.")
        ListenForUser = False

def Transcribe(audio):
    global ListenForUser

    try:
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = transcribe_with_whisper('prompt.wav')
        UserQuery = result['text']
        if len(UserQuery.strip()) == 0:
            print("Empty prompt. Please speak again.")
            ListenForUser = True
        else:
            ListenForUser = True
            return UserQuery
    
    except Exception as e:
        print("Prompt error: ", e)
    

def callback(recognizer, audio):
    global ListenForUser
    global bing_engine
    if ListenForUser:
        HasUserAsked(audio)
    else:
        Text = Transcribe(audio)
        print(Text)


def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    print('\nHey Jarvis or Vision to Start \n')
    r.listen_in_background(source, callback)
    while True:
        time.sleep(1) 

if __name__ == '__main__':
    start_listening() 