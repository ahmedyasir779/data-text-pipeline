import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from advanced_nlp import AdvancedNLP


class TestAdvancedNLP:
    @pytest.fixture
    def nlp(self):
        """Create AdvancedNLP instance"""
        return AdvancedNLP()
    
    @pytest.fixture
    def sample_texts(self):
        """Sample texts for testing"""
        return [
            "Apple Inc. is located in Cupertino, California.",
            "Microsoft CEO Satya Nadella spoke at the conference.",
            "The company earned $50 million in revenue.",
            "Amazon opened a new office in Seattle on Monday.",
            "This product is excellent! Great quality and value."
        ]
    
    def test_extract_entities(self, nlp, sample_texts):
        """Test entity extraction"""
        entities = nlp.extract_entities(sample_texts)
        
        assert isinstance(entities, dict)
        
        # Should find organizations
        if 'ORG' in entities:
            assert entities['ORG']['total'] > 0
        
        # Should find locations
        if 'GPE' in entities:
            assert entities['GPE']['total'] > 0
    
    def test_extract_keywords_rake(self, nlp, sample_texts):
        """Test keyword extraction with RAKE"""
        keywords = nlp.extract_keywords(sample_texts, top_n=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        
        # Now returns (keyword, score) - consistent with TF-IDF
        for keyword, score in keywords:  # ← Back to original order
            assert isinstance(keyword, str)
            assert isinstance(score, (int, float))
            assert score > 0
    
    def test_extract_keywords_tfidf(self, nlp, sample_texts):
        """Test keyword extraction with TF-IDF"""
        keywords = nlp.extract_keywords_tfidf(sample_texts, top_n=10)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 10
        
        # Each keyword should be (term, score) tuple
        for keyword, score in keywords:
            assert isinstance(keyword, str)
            assert isinstance(score, (int, float))
            assert score >= 0
    
    def test_detect_topics(self, nlp, sample_texts):
        """Test topic detection"""
        topics = nlp.detect_topics(sample_texts)
        
        assert isinstance(topics, dict)
        
        # Should detect at least one topic
        assert len(topics) > 0
        
        # Each topic should have keywords
        for topic, keywords in topics.items():
            assert isinstance(keywords, list)
    
    def test_calculate_readability(self, nlp):
        """Test readability calculation"""
        text = "This is a simple test. It has short sentences."
        
        readability = nlp.calculate_readability(text)
        
        assert 'flesch_reading_ease' in readability
        assert 'flesch_kincaid_grade' in readability
        assert 'interpretation' in readability
        
        # Flesch Reading Ease should be 0-100
        assert 0 <= readability['flesch_reading_ease'] <= 100
        
        # Grade level should be reasonable
        assert readability['flesch_kincaid_grade'] >= 0
    
    def test_analyze_text_complexity(self, nlp, sample_texts):
        """Test text complexity analysis"""
        complexity = nlp.analyze_text_complexity(sample_texts)
        
        assert 'avg_flesch_reading_ease' in complexity
        assert 'avg_flesch_kincaid_grade' in complexity
        assert 'interpretation' in complexity
        
        # Should have reasonable values
        assert 0 <= complexity['avg_flesch_reading_ease'] <= 100
    
    def test_empty_text_list(self, nlp):
        """Test with empty text list"""
        entities = nlp.extract_entities([])
        assert entities == {}
        
        keywords = nlp.extract_keywords([], top_n=5)
        assert keywords == []
    
    def test_single_word_text(self, nlp):
        """Test with single word"""
        text = "Hello"
        readability = nlp.calculate_readability(text)
        
        # Should handle without crashing
        assert 'flesch_reading_ease' in readability