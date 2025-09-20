import re
import requests
from typing import Dict, List, Optional
import time

class FactChecker:
    """
    Simple fact-checking system using web search and pattern matching
    """
    
    def __init__(self):
        self.suspicious_keywords = [
            'breaking', 'urgent', 'shocking', 'leaked', 'exposed',
            'they don\'t want you to know', 'mainstream media won\'t tell you',
            'doctors hate this', 'miracle cure', 'secret',
            '100% proven', 'studies show', 'experts say'
        ]
        
        self.reliable_sources = [
            'reuters.com', 'ap.org', 'bbc.com', 'cnn.com', 'npr.org',
            'factcheck.org', 'snopes.com', 'politifact.com',
            'who.int', 'cdc.gov', 'nih.gov'
        ]
    
    def analyze_tweet(self, tweet_text: str) -> Dict:
        """
        Analyze a tweet for potential misinformation
        Returns a dictionary with verification results
        """
        result = {
            'text': tweet_text,
            'confidence': 0.5,
            'status': 'unclear',  # 'verified', 'disputed', 'unclear'
            'reasoning': [],
            'sources': [],
            'flags': []
        }
        
        # Check for suspicious patterns
        flags = self._check_suspicious_patterns(tweet_text)
        result['flags'] = flags
        
        # Adjust confidence based on flags
        if flags:
            result['confidence'] -= len(flags) * 0.1
            result['reasoning'].append(f"Contains {len(flags)} suspicious pattern(s)")
        
        # Check for URLs and analyze them
        urls = self._extract_urls(tweet_text)
        if urls:
            url_analysis = self._analyze_urls(urls)
            result['sources'] = url_analysis['sources']
            result['confidence'] += url_analysis['confidence_adjustment']
            result['reasoning'].extend(url_analysis['reasoning'])
        
        # Determine final status
        if result['confidence'] >= 0.7:
            result['status'] = 'verified'
        elif result['confidence'] <= 0.3:
            result['status'] = 'disputed'
        else:
            result['status'] = 'unclear'
        
        return result
    
    def _check_suspicious_patterns(self, text: str) -> List[str]:
        """Check for suspicious keywords and patterns"""
        flags = []
        text_lower = text.lower()
        
        for keyword in self.suspicious_keywords:
            if keyword in text_lower:
                flags.append(f"suspicious_keyword: {keyword}")
        
        # Check for excessive punctuation/caps
        if len(re.findall(r'[!]{2,}', text)) > 0:
            flags.append("excessive_exclamation")
        
        if len(re.findall(r'[A-Z]{4,}', text)) > 2:
            flags.append("excessive_caps")
        
        # Check for numbers without context (often misleading statistics)
        if len(re.findall(r'\d+%', text)) > 2:
            flags.append("many_percentages")
        
        return flags
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from tweet text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def _analyze_urls(self, urls: List[str]) -> Dict:
        """Analyze URLs for reliability"""
        analysis = {
            'sources': [],
            'confidence_adjustment': 0,
            'reasoning': []
        }
        
        for url in urls:
            domain = self._extract_domain(url)
            if domain:
                analysis['sources'].append(domain)
                
                if domain in self.reliable_sources:
                    analysis['confidence_adjustment'] += 0.2
                    analysis['reasoning'].append(f"Contains link to reliable source: {domain}")
                elif self._is_suspicious_domain(domain):
                    analysis['confidence_adjustment'] -= 0.2
                    analysis['reasoning'].append(f"Contains link to questionable source: {domain}")
        
        return analysis
    
    def _extract_domain(self, url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc.lower().replace('www.', '')
        except:
            return None
    
    def _is_suspicious_domain(self, domain: str) -> bool:
        """Check if domain is known for misinformation"""
        suspicious_domains = [
            'fakenews.com', 'clickbait.com', 'conspiracy.net',
            # Add more as needed
        ]
        return domain in suspicious_domains
    
    def generate_response(self, analysis: Dict, original_user: str) -> str:
        """Generate appropriate response based on analysis"""
        confidence = analysis['confidence']
        status = analysis['status']
        
        if status == 'verified':
            response = f"@{original_user} ✅ This appears to be accurate information. "
            if analysis['sources']:
                response += f"Sources include reliable outlets like {', '.join(analysis['sources'][:2])}."
        
        elif status == 'disputed':
            response = f"@{original_user} ⚠️ This claim appears questionable. "
            if analysis['flags']:
                response += f"Contains warning signs: {len(analysis['flags'])} red flags detected. "
            response += "Please verify with reliable sources before sharing."
        
        else:  # unclear
            response = f"@{original_user} 🤔 I cannot verify this claim with confidence. "
            response += "Please check multiple reliable sources before accepting as fact."
        
        # Add reasoning if space allows (Twitter has 280 char limit)
        if len(response) < 200 and analysis['reasoning']:
            reason = analysis['reasoning'][0][:50] + "..." if len(analysis['reasoning'][0]) > 50 else analysis['reasoning'][0]
            response += f" ({reason})"
        
        return response[:280]  # Ensure within Twitter limit