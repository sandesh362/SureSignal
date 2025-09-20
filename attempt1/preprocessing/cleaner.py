import re
import nltk
from nltk.corpus import stopwords

# Download stopwords with error handling
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("📦 Downloading NLTK stopwords...")
    nltk.download("stopwords", quiet=True)

try:
    STOPWORDS = set(stopwords.words("english"))
except Exception as e:
    print(f"⚠️ Could not load stopwords: {e}")
    STOPWORDS = set()

# Try to load spaCy model with fallback
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    SPACY_AVAILABLE = True
except (ImportError, OSError) as e:
    print(f"⚠️ spaCy not available: {e}")
    print("💡 Install with: python -m spacy download en_core_web_sm")
    SPACY_AVAILABLE = False

def clean_text(text: str) -> str:
    """
    Clean and normalize text for NLP processing.
    Steps:
      - Lowercasing
      - Remove URLs, mentions, hashtags, numbers
      - Remove punctuation/special chars
      - Remove stopwords
      - Lemmatization (if spaCy available)
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove mentions, hashtags
    text = re.sub(r"@\w+|#\w+", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove emojis/special chars
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    if SPACY_AVAILABLE:
        # Lemmatization + stopword removal with spaCy
        doc = nlp(text)
        cleaned = " ".join([
            token.lemma_ for token in doc 
            if token.lemma_ not in STOPWORDS and len(token.lemma_) > 2
        ])
    else:
        # Basic stopword removal without lemmatization
        words = text.split()
        cleaned = " ".join([
            word for word in words 
            if word not in STOPWORDS and len(word) > 2
        ])

    return cleaned.strip()