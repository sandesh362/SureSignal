from django.core.management.base import BaseCommand
from django.conf import settings
import os
import yaml

class Command(BaseCommand):
    help = 'Setup the misinformation detection pipeline'

    def add_arguments(self, parser):
        parser.add_argument('--create-config', action='store_true',
                          help='Create a sample configuration file')
        parser.add_argument('--check-deps', action='store_true',
                          help='Check if all dependencies are installed')
        parser.add_argument('--download-models', action='store_true',
                          help='Download required NLP models')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 Setting up Misinformation Detection Pipeline...')
        )

        if options['create_config']:
            self.create_config_file()

        if options['check_deps']:
            self.check_dependencies()

        if options['download_models']:
            self.download_nlp_models()

        self.stdout.write(
            self.style.SUCCESS('✅ Setup completed!')
        )

    def create_config_file(self):
        """Create a sample configuration file"""
        config_path = os.path.join(settings.BASE_DIR, 'config.yaml')
        
        if os.path.exists(config_path):
            self.stdout.write(
                self.style.WARNING('⚠️ Configuration file already exists')
            )
            return

        sample_config = {
            'mongodb': {
                'connection_string': 'mongodb://localhost:27017',
                'database': 'misinformation_db'
            },
            'twitter': {
                'bearer_token': 'your_twitter_bearer_token_here'
            },
            'newsapi': {
                'api_key': 'your_newsapi_key_here'
            },
            'django': {
                'secret_key': 'your-secret-key-here',
                'debug': True,
                'allowed_hosts': ['localhost', '127.0.0.1']
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Created configuration file: {config_path}')
        )
        self.stdout.write(
            self.style.WARNING('⚠️ Please update the API keys in config.yaml')
        )

    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        dependencies = [
            ('django', 'Django'),
            ('pymongo', 'PyMongo'),
            ('tweepy', 'Tweepy'),
            ('newsapi', 'NewsAPI Python'),
            ('nltk', 'NLTK'),
            ('yaml', 'PyYAML'),
        ]

        optional_dependencies = [
            ('spacy', 'spaCy'),
            ('celery', 'Celery'),
            ('redis', 'Redis'),
        ]

        self.stdout.write('🔍 Checking required dependencies...')
        
        missing_required = []
        for module, name in dependencies:
            try:
                __import__(module)
                self.stdout.write(f'  ✅ {name}')
            except ImportError:
                self.stdout.write(f'  ❌ {name}')
                missing_required.append(name)

        self.stdout.write('\n🔍 Checking optional dependencies...')
        
        missing_optional = []
        for module, name in optional_dependencies:
            try:
                __import__(module)
                self.stdout.write(f'  ✅ {name}')
            except ImportError:
                self.stdout.write(f'  ⚠️ {name} (optional)')
                missing_optional.append(name)

        if missing_required:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Missing required dependencies: {", ".join(missing_required)}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ All required dependencies are installed')
            )

        if missing_optional:
            self.stdout.write(
                self.style.WARNING(f'\n⚠️ Missing optional dependencies: {", ".join(missing_optional)}')
            )

    def download_nlp_models(self):
        """Download required NLP models"""
        self.stdout.write('📦 Downloading NLP models...')
        
        # Download NLTK data
        try:
            import nltk
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            self.stdout.write('  ✅ NLTK stopwords and punkt')
        except Exception as e:
            self.stdout.write(f'  ❌ NLTK download failed: {e}')

        # Download spaCy model
        try:
            import subprocess
            result = subprocess.run([
                'python', '-m', 'spacy', 'download', 'en_core_web_sm'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.stdout.write('  ✅ spaCy en_core_web_sm model')
            else:
                self.stdout.write('  ⚠️ spaCy model download failed (optional)')
        except Exception as e:
            self.stdout.write(f'  ⚠️ spaCy model download failed: {e}')