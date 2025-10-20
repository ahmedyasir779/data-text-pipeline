import pytest
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unified_pipeline import UnifiedPipeline


class TestUnifiedPipeline:
    def test_initialization(self):
        """Test pipeline initialization"""
        pipeline = UnifiedPipeline(use_cache=False)
        
        assert pipeline.data_df is None
        assert pipeline.text_data == []
        assert pipeline.results == {}
    
    def test_load_structured_data(self, sample_csv_path):
        """Test loading structured data"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        
        assert pipeline.data_df is not None
        assert len(pipeline.data_df) == 5
        assert len(pipeline.data_df.columns) == 4
    
    def test_load_nonexistent_file(self):
        """Test loading file that doesn't exist"""
        pipeline = UnifiedPipeline(use_cache=False)
        
        with pytest.raises(FileNotFoundError):
            pipeline.load_structured_data('nonexistent.csv')
    
    def test_load_text_column(self, sample_csv_path):
        """Test extracting text from column"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        pipeline.load_text_column('review')
        
        assert len(pipeline.text_data) == 5
        assert all(isinstance(text, str) for text in pipeline.text_data)
    
    def test_load_invalid_text_column(self, sample_csv_path):
        """Test loading invalid column"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        
        with pytest.raises(ValueError):
            pipeline.load_text_column('nonexistent_column')
    
    def test_clean_data(self, sample_csv_path):
        """Test data cleaning"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        
        original_len = len(pipeline.data_df)
        pipeline.clean_data()
        
        # Should not crash
        assert pipeline.data_df is not None
        # Length might change if duplicates removed
        assert len(pipeline.data_df) <= original_len
    
    def test_analyze_data(self, sample_csv_path):
        """Test data analysis"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        pipeline.analyze_data()
        
        assert 'data_statistics' in pipeline.results
        stats = pipeline.results['data_statistics']
        
        # Should have statistics for numeric columns
        assert 'rating' in stats
        assert 'mean' in stats['rating']
        assert 'median' in stats['rating']
    
    def test_analyze_text(self, sample_csv_path):
        """Test text analysis"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        pipeline.load_text_column('review')
        pipeline.analyze_text()
        
        assert 'text_statistics' in pipeline.results
        stats = pipeline.results['text_statistics']
        
        assert 'total_entries' in stats
        assert 'total_words' in stats
        assert 'unique_words' in stats
        assert stats['total_entries'] == 5
    
    def test_analyze_sentiment(self, sample_csv_path):
        """Test sentiment analysis"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        pipeline.load_text_column('review')
        pipeline.analyze_sentiment()
        
        assert 'sentiment' in pipeline.results
        sentiment = pipeline.results['sentiment']
        
        assert 'avg_polarity' in sentiment
        assert 'positive_count' in sentiment
        assert 'negative_count' in sentiment
        assert sentiment['total'] == 5
    
    def test_method_chaining(self, sample_csv_path):
        """Test method chaining works"""
        pipeline = UnifiedPipeline(use_cache=False)
        
        result = (pipeline
                  .load_structured_data(sample_csv_path)
                  .load_text_column('review')
                  .clean_data()
                  .analyze_data()
                  .analyze_text())
        
        # Should return self
        assert isinstance(result, UnifiedPipeline)
        
        # Should have run all operations
        assert pipeline.data_df is not None
        assert len(pipeline.text_data) > 0
        assert 'data_statistics' in pipeline.results
        assert 'text_statistics' in pipeline.results
    
    def test_generate_report(self, sample_csv_path):
        """Test report generation"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        pipeline.load_text_column('review')
        pipeline.analyze_data()
        pipeline.analyze_text()
        
        report = pipeline.generate_report()
        
        assert isinstance(report, str)
        assert len(report) > 0
        assert 'REPORT' in report.upper()
    
    def test_correlation_analysis(self, sample_csv_path):
        """Test correlation between rating and text length"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        pipeline.load_text_column('review')
        pipeline.correlate_data_with_text_length('rating')
        
        assert 'correlation' in pipeline.results
        corr = pipeline.results['correlation']
        assert 'correlation_with_text_length' in corr
        
        # Correlation should be between -1 and 1
        assert -1 <= corr['correlation_with_text_length'] <= 1


class TestPipelineWithCache:
    """Test pipeline with caching enabled"""
    
    def test_cache_enabled(self, sample_csv_path, cache_dir):
        """Test that caching works"""
        pipeline = UnifiedPipeline(use_cache=True)
        
        # First load (no cache)
        pipeline.load_structured_data(sample_csv_path)
        
        # Second load (should use cache)
        pipeline2 = UnifiedPipeline(use_cache=True)
        pipeline2.load_structured_data(sample_csv_path)
        
        # Data should be identical
        assert len(pipeline.data_df) == len(pipeline2.data_df)
    
    def test_cache_disabled(self, sample_csv_path):
        """Test pipeline with cache disabled"""
        pipeline = UnifiedPipeline(use_cache=False)
        
        assert pipeline.cache is None
        
        # Should still work
        pipeline.load_structured_data(sample_csv_path)
        assert pipeline.data_df is not None


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.data_df = pd.DataFrame()
        
        # Should handle gracefully
        pipeline.analyze_data()
        # Shouldn't crash
    
    def test_no_numeric_columns(self):
        """Test with no numeric columns"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.data_df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'city': ['NYC', 'LA']
        })
        
        pipeline.analyze_data()
        # Should handle gracefully
    
    def test_no_text_data(self, sample_csv_path):
        """Test operations without text data"""
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(sample_csv_path)
        
        # Should handle gracefully
        pipeline.analyze_text()  # No text loaded
        pipeline.analyze_sentiment()  # No text loaded
        
        # Shouldn't crash
    
    def test_single_row(self, tmp_path):
        """Test with single row of data"""
        single_row = pd.DataFrame({
            'text': ['Single text entry'],
            'value': [42]
        })
        
        csv_path = tmp_path / "single.csv"
        single_row.to_csv(csv_path, index=False)
        
        pipeline = UnifiedPipeline(use_cache=False)
        pipeline.load_structured_data(str(csv_path))
        pipeline.load_text_column('text')
        pipeline.analyze_text()
        
        assert 'text_statistics' in pipeline.results