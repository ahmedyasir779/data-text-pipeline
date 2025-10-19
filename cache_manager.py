import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Optional
import pandas as pd


class CacheManager:
    def __init__(self, cache_dir: str = '.cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.cache_dir / 'data').mkdir(exist_ok=True)
        (self.cache_dir / 'analysis').mkdir(exist_ok=True)
        (self.cache_dir / 'nlp').mkdir(exist_ok=True)
        
        print(f"✓ Cache initialized at {self.cache_dir}")
    
    def _generate_key(self, data: Any) -> str:
        """
        Generate cache key from data
        
        Args:
            data: Data to hash
            
        Returns:
            Hash string
        """
        if isinstance(data, pd.DataFrame):
            # Hash DataFrame by converting to string
            data_str = str(data.values.tobytes())
        elif isinstance(data, list):
            # Hash list content
            data_str = str(data)
        elif isinstance(data, str):
            # For file paths, check if it's actually a file path
            # Only check file existence if it looks like a path (no quotes, reasonable length)
            if len(data) < 255 and not data.startswith('[') and Path(data).exists():
                # It's a file path - include modification time
                mtime = Path(data).stat().st_mtime
                data_str = f"{data}_{mtime}"
            else:
                # It's just a string (not a file path)
                data_str = data
        else:
            data_str = str(data)
        
        # Return MD5 hash (always short and safe for filenames)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get(self, key: str, category: str = 'data') -> Optional[Any]:
        """
        Get item from cache
        
        Args:
            key: Cache key
            category: Cache category (data, analysis, nlp)
            
        Returns:
            Cached data or None if not found
        """
        cache_path = self.cache_dir / category / f"{key}.pkl"
        
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"⚠ Cache read error: {e}")
                return None
        
        return None
    
    def set(self, key: str, data: Any, category: str = 'data'):
        """
        Store item in cache
        
        Args:
            key: Cache key
            data: Data to cache
            category: Cache category (data, analysis, nlp)
        """
        cache_path = self.cache_dir / category / f"{key}.pkl"
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"⚠ Cache write error: {e}")
    
    def exists(self, key: str, category: str = 'data') -> bool:
        """
        Check if cache entry exists
        
        Args:
            key: Cache key
            category: Cache category
            
        Returns:
            True if exists, False otherwise
        """
        cache_path = self.cache_dir / category / f"{key}.pkl"
        return cache_path.exists()
    
    def clear(self, category: Optional[str] = None):
        """
        Clear cache
        
        Args:
            category: Category to clear, or None for all
        """
        if category:
            cache_dir = self.cache_dir / category
            for file in cache_dir.glob('*.pkl'):
                file.unlink()
            print(f"✓ Cleared {category} cache")
        else:
            for category_dir in self.cache_dir.iterdir():
                if category_dir.is_dir():
                    for file in category_dir.glob('*.pkl'):
                        file.unlink()
            print("✓ Cleared all caches")
    
    def get_cache_size(self) -> dict:
        """
        Get cache size statistics
        
        Returns:
            Dictionary with cache sizes
        """
        sizes = {}
        
        for category_dir in self.cache_dir.iterdir():
            if category_dir.is_dir():
                total_size = sum(f.stat().st_size for f in category_dir.glob('*.pkl'))
                file_count = len(list(category_dir.glob('*.pkl')))
                sizes[category_dir.name] = {
                    'size_mb': round(total_size / (1024 * 1024), 2),
                    'file_count': file_count
                }
        
        return sizes


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CACHE MANAGER - TEST")
    print("=" * 60)
    
    # Initialize
    cache = CacheManager()
    
    # Test caching
    test_data = {'key': 'value', 'numbers': [1, 2, 3]}
    key = cache._generate_key(str(test_data))
    
    print("\n1 Storing data in cache...")
    cache.set(key, test_data, category='data')
    print(f"   Key: {key}")
    
    print("\n2 Retrieving from cache...")
    retrieved = cache.get(key, category='data')
    print(f"   Retrieved: {retrieved}")
    print(f"   Match: {retrieved == test_data}")
    
    print("\n3 Cache statistics...")
    stats = cache.get_cache_size()
    for category, info in stats.items():
        print(f"   {category}: {info['file_count']} files, {info['size_mb']} MB")
    
    print("\n4 Clearing cache...")
    cache.clear()
    
    print("\n" + "=" * 60)
    print("✓ TEST COMPLETE")
    print("=" * 60)