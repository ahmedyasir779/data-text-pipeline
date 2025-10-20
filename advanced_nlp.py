import spacy
from typing import List, Dict, Tuple
from collections import Counter
import re
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class AdvancedNLP:

    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            print(" spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Initialize keyword extractor
        self.rake = Rake()
        
        print(" Advanced NLP initialized")
    
    # ============================================
    # NAMED ENTITY RECOGNITION
    # ============================================
    
    def extract_entities(self, texts: List[str]) -> Dict:
        """
        Extract named entities from texts
        
        Args:
            texts: List of text strings
            
        Returns:
            Dictionary with entity types and counts
        """
        if not self.nlp:
            print("⚠ spaCy model not available")
            return {}
        
        all_entities = {
            'PERSON': [],      # People names
            'ORG': [],         # Organizations
            'GPE': [],         # Countries, cities, states
            'PRODUCT': [],     # Products
            'DATE': [],        # Dates
            'MONEY': [],       # Money amounts
            'LOC': [],         # Locations (non-GPE)
            'EVENT': [],       # Events
        }
        
        for text in texts:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in all_entities:
                    all_entities[ent.label_].append(ent.text)
        
        # Count frequencies
        entity_counts = {}
        for entity_type, entities in all_entities.items():
            if entities:
                counter = Counter(entities)
                entity_counts[entity_type] = {
                    'total': len(entities),
                    'unique': len(counter),
                    'top_5': counter.most_common(5)
                }
        
        return entity_counts
    
    def get_top_entities(self, texts: List[str], entity_type: str = 'PERSON', top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Get top N entities of a specific type
        
        Args:
            texts: List of text strings
            entity_type: Type of entity (PERSON, ORG, GPE, etc.)
            top_n: Number of top entities to return
            
        Returns:
            List of (entity, count) tuples
        """
        if not self.nlp:
            return []
        
        entities = []
        for text in texts:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == entity_type:
                    entities.append(ent.text)
        
        counter = Counter(entities)
        return counter.most_common(top_n)
    
    # ============================================
    # KEYWORD EXTRACTION
    # ============================================
    
    def extract_keywords(self, texts: List[str], top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords using RAKE algorithm
        
        Args:
            texts: List of text strings
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, score) tuples
        """
        # Combine all texts
        combined_text = ' '.join(texts)
        
        # Extract keywords
        self.rake.extract_keywords_from_text(combined_text)
        keywords_raw = self.rake.get_ranked_phrases_with_scores()
        
        # RAKE returns (score, phrase) - reverse to (phrase, score) for consistency
        keywords = [(phrase, score) for score, phrase in keywords_raw[:top_n]]
        
        return keywords
    
    
    def extract_keywords_tfidf(self, texts: List[str], top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords using TF-IDF
        
        Args:
            texts: List of text strings
            top_n: Number of top keywords per document
            
        Returns:
            List of (keyword, score) tuples (averaged across documents)
        """
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)  # Unigrams and bigrams
        )
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get average scores across all documents
        avg_scores = np.mean(tfidf_matrix.toarray(), axis=0)
        
        # Sort by score
        top_indices = avg_scores.argsort()[-top_n:][::-1]
        
        keywords = [(feature_names[i], avg_scores[i]) for i in top_indices]
        
        return keywords
    
    # ============================================
    # TOPIC DETECTION
    # ============================================
    
    def detect_topics(self, texts: List[str]) -> Dict:
        """
        Detect main topics in texts using simple keyword clustering
        
        Args:
            texts: List of text strings
            
        Returns:
            Dictionary with detected topics
        """
        # Extract keywords
        keywords = self.extract_keywords_tfidf(texts, top_n=20)
        
        # Simple topic categorization based on common themes
        topics = {
            'quality': [],
            'price': [],
            'service': [],
            'features': [],
            'experience': [],
            'other': []
        }
        
        quality_terms = ['quality', 'good', 'excellent', 'poor', 'bad', 'great', 'terrible', 'amazing']
        price_terms = ['price', 'expensive', 'cheap', 'cost', 'value', 'worth', 'money']
        service_terms = ['service', 'support', 'customer', 'help', 'response', 'staff']
        feature_terms = ['feature', 'function', 'work', 'performance', 'speed', 'design']
        experience_terms = ['use', 'easy', 'difficult', 'simple', 'experience', 'recommend']
        
        for keyword, score in keywords:
            keyword_lower = keyword.lower()
            
            if any(term in keyword_lower for term in quality_terms):
                topics['quality'].append((keyword, score))
            elif any(term in keyword_lower for term in price_terms):
                topics['price'].append((keyword, score))
            elif any(term in keyword_lower for term in service_terms):
                topics['service'].append((keyword, score))
            elif any(term in keyword_lower for term in feature_terms):
                topics['features'].append((keyword, score))
            elif any(term in keyword_lower for term in experience_terms):
                topics['experience'].append((keyword, score))
            else:
                topics['other'].append((keyword, score))
        
        # Remove empty topics
        topics = {k: v for k, v in topics.items() if v}
        
        return topics
    
    # ============================================
    # TEXT COMPLEXITY METRICS
    # ============================================
    
    def calculate_readability(self, text: str) -> Dict:
        """
        Calculate readability metrics
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with readability scores
        """
        # Count sentences, words, syllables
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = text.split()
        
        # Simple syllable counter (approximation)
        def count_syllables(word):
            word = word.lower()
            vowels = 'aeiou'
            count = 0
            previous_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not previous_was_vowel:
                    count += 1
                previous_was_vowel = is_vowel
            
            # Adjust for silent e
            if word.endswith('e'):
                count -= 1
            
            return max(1, count)
        
        syllables = sum(count_syllables(word) for word in words)
        
        # Calculate metrics
        num_sentences = len(sentences)
        num_words = len(words)
        num_syllables = syllables
        
        if num_sentences == 0 or num_words == 0:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'avg_words_per_sentence': 0,
                'avg_syllables_per_word': 0
            }
        
        avg_words_per_sentence = num_words / num_sentences
        avg_syllables_per_word = num_syllables / num_words
        
        # Flesch Reading Ease (0-100, higher = easier)
        flesch_reading_ease = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
        flesch_reading_ease = max(0, min(100, flesch_reading_ease))
        
        # Flesch-Kincaid Grade Level
        flesch_kincaid_grade = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
        flesch_kincaid_grade = max(0, flesch_kincaid_grade)
        
        return {
            'flesch_reading_ease': round(flesch_reading_ease, 2),
            'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'interpretation': self._interpret_readability(flesch_reading_ease)
        }
    
    def _interpret_readability(self, score: float) -> str:
        """Interpret Flesch Reading Ease score"""
        if score >= 90:
            return "Very easy (5th grade)"
        elif score >= 80:
            return "Easy (6th grade)"
        elif score >= 70:
            return "Fairly easy (7th grade)"
        elif score >= 60:
            return "Standard (8th-9th grade)"
        elif score >= 50:
            return "Fairly difficult (10th-12th grade)"
        elif score >= 30:
            return "Difficult (College)"
        else:
            return "Very difficult (College graduate)"
    
    def analyze_text_complexity(self, texts: List[str]) -> Dict:
        """
        Analyze complexity of all texts
        
        Args:
            texts: List of text strings
            
        Returns:
            Dictionary with aggregated complexity metrics
        """
        all_readability = [self.calculate_readability(text) for text in texts]
        
        avg_flesch = np.mean([r['flesch_reading_ease'] for r in all_readability])
        avg_grade = np.mean([r['flesch_kincaid_grade'] for r in all_readability])
        avg_words_per_sentence = np.mean([r['avg_words_per_sentence'] for r in all_readability])
        
        return {
            'avg_flesch_reading_ease': round(avg_flesch, 2),
            'avg_flesch_kincaid_grade': round(avg_grade, 2),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'interpretation': self._interpret_readability(avg_flesch),
            'readability_scores': all_readability
        }


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("ADVANCED NLP - TEST")
    print("=" * 60)
    
    # Sample texts
    test_texts = [
        "Apple Inc. announced record profits today. CEO Tim Cook spoke at the event in Cupertino, California.",
        "Microsoft is expanding its operations in Seattle. The company plans to invest $500 million.",
        "Google's new product launch was successful. Many customers praised the excellent quality and features.",
        "Amazon's customer service is outstanding. Fast delivery and great support make shopping easy.",
        "The product quality is terrible. Very disappointed with the poor design and high price."
    ]
    
    # Initialize
    nlp = AdvancedNLP()
    
    # Test entity extraction
    print("\n NAMED ENTITY RECOGNITION")
    print("-" * 60)
    entities = nlp.extract_entities(test_texts)
    
    for entity_type, data in entities.items():
        print(f"\n{entity_type}:")
        print(f"  Total: {data['total']}, Unique: {data['unique']}")
        print(f"  Top mentions: {data['top_5'][:3]}")
    
    # Test keyword extraction
    print("\n\n KEYWORD EXTRACTION (RAKE)")
    print("-" * 60)
    keywords_rake = nlp.extract_keywords(test_texts, top_n=10)
    for keyword, score in keywords_rake[:5]:
        print(f"  {keyword}: {score}")
    
    print("\n\n KEYWORD EXTRACTION (TF-IDF)")
    print("-" * 60)
    keywords_tfidf = nlp.extract_keywords_tfidf(test_texts, top_n=10)
    for keyword, score in keywords_tfidf[:5]:
        print(f"  {keyword}: {float(score):.3f}")
    
    # Test topic detection
    print("\n\n TOPIC DETECTION")
    print("-" * 60)
    topics = nlp.detect_topics(test_texts)
    for topic, keywords in topics.items():
        print(f"\n{topic.upper()}:")
        for keyword, score in keywords[:3]:
            print(f"  {keyword}: {float(score):.3f}")
    
    # Test readability
    print("\n\n TEXT COMPLEXITY")
    print("-" * 60)
    complexity = nlp.analyze_text_complexity(test_texts)
    print(f"Average Flesch Reading Ease: {complexity['avg_flesch_reading_ease']}")
    print(f"Average Grade Level: {complexity['avg_flesch_kincaid_grade']}")
    print(f"Interpretation: {complexity['interpretation']}")
    print(f"Avg words per sentence: {complexity['avg_words_per_sentence']}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETE")
    print("=" * 60)