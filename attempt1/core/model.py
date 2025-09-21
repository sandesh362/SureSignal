from djongo import models
from django.utils import timezone

class Tweet(models.Model):
    platform = models.CharField(max_length=50, default='twitter')
    tweet_id = models.CharField(max_length=100, unique=True)
    author_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField()
    lang = models.CharField(max_length=10, null=True, blank=True)
    text = models.TextField()
    cleaned_text = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tweets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Tweet {self.tweet_id} - {self.text[:50]}..."

class NewsArticle(models.Model):
    platform = models.CharField(max_length=50, default='newsapi')
    source = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    cleaned_text = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'news'
        ordering = ['-published_at']
    
    def __str__(self):
        return f"{self.title} - {self.source}"
