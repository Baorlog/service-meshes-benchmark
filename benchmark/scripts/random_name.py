import random

adjectives = [
    "admiring", "adoring", "affectionate", "agitated", "amazing",
    "angry", "awesome", "blissful", "bold", "brave", "busy", "charming"
]

scientists = [
    "curie", "einstein", "tesla", "turing", "morse", "hawking",
    "newton", "galileo", "pasteur", "lovelace", "fermi", "archimedes"
]

def generate_random_name():
    return f"{random.choice(adjectives)}_{random.choice(scientists)}"
