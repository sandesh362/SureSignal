import pymongo
from django.conf import settings
import yaml
import os

class DatabaseManager:
    _instance = None
    _client = None
    _db = None
    _connected = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            # Get MongoDB configuration from Django settings or config
            if hasattr(settings, 'DATABASES') and 'default' in settings.DATABASES:
                mongo_config = settings.DATABASES['default']['CLIENT']
                connection_string = mongo_config.get('host', 'mongodb://localhost:27017')
                database_name = settings.DATABASES['default']['NAME']
            else:
                # Fallback to direct config loading
                config_path = os.path.join(settings.BASE_DIR, 'config.yaml')
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                connection_string = config['mongodb']['connection_string']
                database_name = config['mongodb']['database']
            
            self._client = pymongo.MongoClient(connection_string)
            self._db = self._client[database_name]
            
            # Test connection
            self._client.admin.command('ping')
            self._connected = True
            print(f"✅ Connected to MongoDB: {database_name}")
            
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self._connected = False
    
    @property
    def db(self):
        return self._db
    
    @property
    def connected(self):
        return self._connected
    
    def get_collection(self, collection_name):
        if self._connected:
            return self._db[collection_name]
        return None

# Create singleton instance
db_manager = DatabaseManager()

# core/serializers.py
from rest_framework import serializers
from .models import Tweet, NewsArticle

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'