import time
from unified_pipeline import UnifiedPipeline

def benchmark():
    print("=" * 60)
    print("PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    # Test 1: Without cache
    print("\n1 First run (no cache):")
    pipeline1 = UnifiedPipeline(use_cache=False)
    
    start = time.time()
    pipeline1.load_structured_data('data/customer_reviews.csv')
    pipeline1.load_text_column('review')
    pipeline1.analyze_sentiment()
    pipeline1.extract_entities()
    elapsed_no_cache = time.time() - start
    
    print(f"   Time: {elapsed_no_cache:.2f}s")
    
    # Test 2: With cache (first run)
    print("\n2 First run with cache:")
    pipeline2 = UnifiedPipeline(use_cache=True)
    
    start = time.time()
    pipeline2.load_structured_data('data/customer_reviews.csv')
    pipeline2.load_text_column('review')
    pipeline2.analyze_sentiment()
    pipeline2.extract_entities()
    elapsed_cache_first = time.time() - start
    
    print(f"   Time: {elapsed_cache_first:.2f}s")
    
    # Test 3: With cache (second run)
    print("\n3 Second run with cache:")
    pipeline3 = UnifiedPipeline(use_cache=True)
    
    start = time.time()
    pipeline3.load_structured_data('data/customer_reviews.csv')
    pipeline3.load_text_column('review')
    pipeline3.analyze_sentiment()
    pipeline3.extract_entities()
    elapsed_cache_second = time.time() - start
    
    print(f"   Time: {elapsed_cache_second:.2f}s")
    
    # Summary
    print("\n" + "=" * 60)
    print("RESULTS:")
    print(f"  No cache: {elapsed_no_cache:.2f}s")
    print(f"  With cache (first): {elapsed_cache_first:.2f}s")
    print(f"  With cache (cached): {elapsed_cache_second:.2f}s")
    print(f"  Speedup: {elapsed_no_cache / elapsed_cache_second:.1f}x faster")
    print("=" * 60)

if __name__ == "__main__":
    benchmark()