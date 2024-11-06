from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from common_terms import CLICKABLE_TERMS

app = Flask(__name__)
app.secret_key = 'Secret'  # Needed for session management

API_KEY = 'c7ee0d40-808a-439c-80cc-ffb99781afaa'
API_URL = 'https://dictionaryapi.com/api/v3/references/medical/json/'

THESAURUS_API_KEY = '94e838be-88ae-4418-8063-ca5d441de463'
THESAURUS_API_URL = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/'

# Initialize an in-memory list to store favorites for the session
favorites = []

def generate_audio_url(audio_filename):
    """Generates the correct audio URL based on Merriam-Webster's guidelines."""
    subdirectory = (
        "bix" if audio_filename.startswith("bix") else
        "gg" if audio_filename.startswith("gg") else
        "number" if audio_filename[0].isdigit() or audio_filename[0] == "_" else
        audio_filename[0]
    )
    return f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdirectory}/{audio_filename}.mp3"

def format_pronunciations(pronunciations):
    """Formats pronunciations with labels and punctuation according to the API guidelines."""
    formatted_prons = []
    for pron in pronunciations:
        # Extract components of each pronunciation
        mw = pron.get('mw', '')
        l = f"<i>{pron['l']}</i> " if 'l' in pron else ""
        l2 = f" <i>{pron['l2']}</i>" if 'l2' in pron else ""
        # Format pronunciation
        formatted_pron = f"{l}{mw}{l2}"
        formatted_prons.append(formatted_pron)

    # Join pronunciations with specified punctuation
    separator = pronunciations[0].get('pun', ', ') if len(pronunciations) > 1 else ""
    return f"\\{separator.join(formatted_prons)}\\"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        term = request.form.get('term')
        if term:
            return redirect(url_for('result', term=term))
    return render_template('index.html')


def get_related_terms(data):

# Check if 'data' is a list
    if isinstance(data, list):
        # Assuming you want to access the first element of the list
        if len(data) > 0 and isinstance(data[0], dict):
            # Now you can safely access the dictionary
            meta_data = data[0].get("meta", {})
            
            # Now check for 'syns' in 'meta_data'
            if "syns" in meta_data and isinstance(meta_data["syns"], list):
                if len(meta_data["syns"]) > 0 and isinstance(meta_data["syns"][0], list):
                    synonyms = meta_data["syns"][0]
                else:
                    synonyms = []
            else:
                synonyms = []
        else:
            synonyms = []  # Handle case where the first element is not a dictionary
    else:
        # Handle the case where data is not a list or is empty
        synonyms = []

    # Print or use the list as needed
    return synonyms


@app.route('/result')
def result():
    term = request.args.get('term')
    if not term:
        return redirect(url_for('index'))

    # Fetch the definition and related terms from Merriam-Webster API
    response = requests.get(f"{API_URL}{term}?key={API_KEY}")
    responset = requests.get(f"{THESAURUS_API_URL}{term}?key={THESAURUS_API_KEY}")
    if response.status_code == 200:
        data = response.json()
        datat = responset.json()
        
        # Initialize empty values for display
        definition = "Definition not found. Try a different term."
        synonyms = get_related_terms(datat)
        audio_urls = []
        formatted_pronunciations = ""

        # Process the API response
        if isinstance(data, list) and data:
            if isinstance(data[0], str):
                related_terms = data
            elif 'shortdef' in data[0]:
                definition = data[0]['shortdef'][0]

                # Extract pronunciation and audio URLs
                if 'hwi' in data[0] and 'prs' in data[0]['hwi']:
                    prs = data[0]['hwi']['prs']
                    # Format the pronunciation display
                    formatted_pronunciations = format_pronunciations(prs)
                    # Generate audio URLs for each pronunciation
                    for pronunciation in prs:
                        if 'sound' in pronunciation and 'audio' in pronunciation['sound']:
                            audio_url = generate_audio_url(pronunciation['sound']['audio'])
                            audio_urls.append(audio_url)
        else:
            definition = "Error retrieving definition. Please try again later."
    else:
        definition = "Error retrieving definition. Please try again later."

    return render_template('result.html', term=term, definition=definition, related_terms=synonyms  , clickable_terms=CLICKABLE_TERMS, formatted_pronunciations=formatted_pronunciations, audio_urls=audio_urls)

@app.route('/add_favorite/<term>')
def add_favorite(term):
    # Ensure the term is not already in favorites to avoid duplicates
    if term not in favorites:
        favorites.append(term)
    return redirect(url_for('favorites_page'))

@app.route('/favorites')
def favorites_page():
    return render_template('favorites.html', favorites=favorites)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '').lower()
    suggestions = [word for word in CLICKABLE_TERMS if term in word.lower()]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
