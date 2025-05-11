import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Set properties (optional)
    # engine.setProperty('rate', 150)     # Speed of speech
    # engine.setProperty('volume', 1.0)   # Volume level (0.0 to 1.0)
    
    # Speak the text
    engine.say(text)
    
    # Wait for the speech to finish
    engine.runAndWait()

# Example usage
if __name__ == "__main__":
    speak("Hello, how are you today?")
