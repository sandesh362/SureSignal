from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        # Initialize NLTK and spaCy when Django starts
        import nltk
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("📦 Downloading NLTK stopwords...")
            nltk.download("stopwords", quiet=True)