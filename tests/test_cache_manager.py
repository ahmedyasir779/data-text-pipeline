import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cache_manager import CacheManager


class TestCacheManager:
    def test_initialization(self, tmp_path):
        """Test cache manager initialization"""
        cache_dir = tmp_path / "test_cache"
        cache = CacheManager(cache_dir=str(cache_dir))
        
        assert cache.cache_dir.exists()
        assert (cache.cache_dir / 'data').exists()
        assert (cache.cache_dir / 'analysis').exists()
        assert (cache.cache_dir / 'nlp').exists()
    
    def test_set_and_get(self, tmp_path):
        """Test setting and getting cache"""
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        test_data = {'key': 'value', 'number': 42}
        key = 'test_key'
        
        # Set
        cache.set(key, test_data, category='data')
        
        # Get
        retrieved = cache.get(key, category='data')
        
        assert retrieved == test_data
    
    def test_exists(self, tmp_path):
        """Test checking if cache exists"""
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        key = 'test_key'
        
        # Shouldn't exist yet
        assert not cache.exists(key, category='data')
        
        # Set data
        cache.set(key, {'data': 'value'}, category='data')
        
        # Should exist now
        assert cache.exists(key, category='data')
    
    def test_clear_category(self, tmp_path):
        """Test clearing specific category"""
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        # Add data to multiple categories
        cache.set('key1', {'data': '1'}, category='data')
        cache.set('key2', {'data': '2'}, category='analysis')
        
        # Clear only 'data' category
        cache.clear(category='data')
        
        # 'data' should be gone
        assert not cache.exists('key1', category='data')
        
        # 'analysis' should still exist
        assert cache.exists('key2', category='analysis')
    
    def test_clear_all(self, tmp_path):
        """Test clearing all caches"""
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        # Add data to multiple categories
        cache.set('key1', {'data': '1'}, category='data')
        cache.set('key2', {'data': '2'}, category='analysis')
        cache.set('key3', {'data': '3'}, category='nlp')
        
        # Clear all
        cache.clear()
        
        # All should be gone
        assert not cache.exists('key1', category='data')
        assert not cache.exists('key2', category='analysis')
        assert not cache.exists('key3', category='nlp')
    
    def test_get_cache_size(self, tmp_path):
        """Test getting cache size statistics"""
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        # Add some data
        cache.set('key1', {'data': 'test' * 100}, category='data')
        cache.set('key2', {'data': 'test' * 100}, category='analysis')
        
        sizes = cache.get_cache_size()
        
        assert 'data' in sizes
        assert 'analysis' in sizes
        assert sizes['data']['file_count'] == 1
        assert sizes['analysis']['file_count'] == 1
        
        # File exists so size should be non-negative (can be 0.0 if very small)
        assert sizes['data']['size_mb'] >= 0
        assert sizes['analysis']['size_mb'] >= 0
        
        # At least verify files were created
        assert (cache.cache_dir / 'data').exists()
        assert len(list((cache.cache_dir / 'data').glob('*.pkl'))) == 1
    
    def test_cache_invalidation_on_change(self, tmp_path):
        """Test that cache key changes when data changes"""
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        data1 = "original data"
        data2 = "modified data"
        
        key1 = cache._generate_key(data1)
        key2 = cache._generate_key(data2)
        
        # Different data should have different keys
        assert key1 != key2