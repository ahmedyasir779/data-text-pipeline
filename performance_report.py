import time
import matplotlib.pyplot as plt
from unified_pipeline import UnifiedPipeline

def performance_report():
    operations = ['Load Data', 'Sentiment', 'Entities', 'Keywords']
    no_cache_times = []
    cache_times = []
    
    # Test without cache
    print("Testing without cache...")
    pipeline = UnifiedPipeline(use_cache=False)
    
    start = time.time()
    pipeline.load_structured_data('data/customer_reviews.csv')
    no_cache_times.append(time.time() - start)
    
    pipeline.load_text_column('review')
    
    start = time.time()
    pipeline.analyze_sentiment()
    no_cache_times.append(time.time() - start)
    
    start = time.time()
    pipeline.extract_entities()
    no_cache_times.append(time.time() - start)
    
    start = time.time()
    pipeline.extract_keywords()
    no_cache_times.append(time.time() - start)
    
    # Test with cache (cached run)
    print("\nTesting with cache...")
    pipeline2 = UnifiedPipeline(use_cache=True)
    
    start = time.time()
    pipeline2.load_structured_data('data/customer_reviews.csv')
    cache_times.append(time.time() - start)
    
    pipeline2.load_text_column('review')
    
    start = time.time()
    pipeline2.analyze_sentiment()
    cache_times.append(time.time() - start)
    
    start = time.time()
    pipeline2.extract_entities()
    cache_times.append(time.time() - start)
    
    start = time.time()
    pipeline2.extract_keywords()
    cache_times.append(time.time() - start)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart comparison
    x = range(len(operations))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], no_cache_times, width, label='No Cache', color='red', alpha=0.7)
    ax1.bar([i + width/2 for i in x], cache_times, width, label='With Cache', color='green', alpha=0.7)
    ax1.set_xlabel('Operation')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Performance Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(operations, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Speedup chart
    speedups = [no_cache / cache if cache > 0 else 0 for no_cache, cache in zip(no_cache_times, cache_times)]
    ax2.bar(operations, speedups, color='blue', alpha=0.7)
    ax2.set_xlabel('Operation')
    ax2.set_ylabel('Speedup (x times faster)')
    ax2.set_title('Cache Speedup Factor')
    ax2.set_xticklabels(operations, rotation=45, ha='right')
    ax2.axhline(y=1, color='r', linestyle='--', label='No improvement')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/performance_report.png', dpi=300, bbox_inches='tight')
    print("\n✓ Performance report saved to output/performance_report.png")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    total_no_cache = sum(no_cache_times)
    total_cache = sum(cache_times)
    print(f"Total time (no cache): {total_no_cache:.2f}s")
    print(f"Total time (cached): {total_cache:.2f}s")
    print(f"Overall speedup: {total_no_cache/total_cache:.1f}x faster")
    print("=" * 60)

if __name__ == "__main__":
    performance_report()