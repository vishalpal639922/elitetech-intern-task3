import nltk
import spacy
from nltk.chat.util import Chat, reflections
from datetime import datetime
import random
import webbrowser

# Load NLP models
nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')

# Custom reflections for more natural responses
jarvis_reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine"
}

# JARVIS personality responses
greetings = [
    "At your service, sir.",
    "How may I assist you today?",
    "JARVIS online and ready.",
    "Yes, sir?",
    "I'm listening."
]

farewells = [
    "Until next time, sir.",
    "JARVIS signing off.",
    "Always a pleasure, sir.",
    "Shutting down systems.",
    "Goodbye, sir."
]

# Conversation patterns
pairs = [
    [
        r"(hi|hello|hey|greetings|good (morning|afternoon|evening)) jarvis",
        greetings
    ],
    [
        r"what('?s| is) your name(\?)?",
        ["I am JARVIS, your personal assistant.", "You may call me JARVIS, sir."]
    ],
    [
        r"how are you(\?)?",
        ["I'm functioning within normal parameters, sir.", "All systems operational. How may I assist you?"]
    ],
    [
        r"(.*) (time|date)(\?)?",
        [lambda x: f"The current time is {datetime.now().strftime('%H:%M')} and date is {datetime.now().strftime('%Y-%m-%d')}, sir."]
    ],
    [
        r"(open|launch) (.*)",
        [lambda x: webbrowser.open(f"https://www.{x.split(' ')[-1]}.com") or "Opening now, sir."]
    ],
    [
        r"(search|look up) (for )?(.*)",
        [lambda x: webbrowser.open(f"https://www.google.com/search?q={'+'.join(x.split(' ')[2:])}") or "Searching now, sir."]
    ],
    [
        r"(thank you|thanks)",
        ["You're welcome, sir.", "Always happy to assist.", "At your service."]
    ],
    [
        r"(quit|exit|goodbye|shut down)",
        farewells
    ],
    [
        r"(.*)",
        ["I didn't quite catch that, sir. Could you rephrase?", 
         "My protocols don't cover that request yet, sir.",
         "Would you like me to search for that information?"]
    ]
]

class JARVIS(Chat):
    def __init__(self, pairs, reflections):
        super().__init__(pairs, reflections)
        self.name = "JARVIS"
    
    def respond(self, str):
        doc = nlp(str.lower())
        
        # Enhanced entity recognition
        for ent in doc.ents:
            if ent.label_ == "TIME":
                return f"At {ent.text}, sir. Would you like me to set a reminder?"
            if ent.label_ == "DATE":
                return f"Regarding {ent.text}, sir. Should I add it to your calendar?"
        
        # Fallback to pattern matching
        response = super().respond(str)
        if isinstance(response, list):
            return random.choice(response)
        return response

def main():
    print("Initializing JARVIS...")
    print("JARVIS: Good day, sir. How may I be of service?")
    jarvis = JARVIS(pairs, jarvis_reflections)
    jarvis.converse()

if __name__ == "__main__":
    main()
