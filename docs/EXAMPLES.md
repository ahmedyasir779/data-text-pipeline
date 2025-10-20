# Usage Examples

## Basic Examples

### Example 1: Simple Analysis
```bash
python cli.py --data-file data.csv --text-column comments --all
```

### Example 2: Sentiment Only
```bash
python cli.py --data-file reviews.csv --text-column review --sentiment
```

### Example 3: Export Results
```bash
python cli.py --data-file data.csv --text-column text --all --export csv
```

## Advanced Examples

### Example 4: Custom Configuration

**config.json:**
```json
{
  "pipeline": {
    "use_cache": true,
    "analyze_sentiment": true,
    "extract_entities": true
  }
}
```

**Run:**
```bash
python cli.py --data-file data.csv --text-column text --config config.json
```

### Example 5: Batch Processing
```bash
# Process all files in directory
python cli.py --batch ./monthly_reports --text-column feedback --all
```

### Example 6: Python API
```python
from unified_pipeline import UnifiedPipeline

# Initialize with caching
pipeline = UnifiedPipeline(use_cache=True)

# Load and process
pipeline.load_structured_data('customer_data.csv')
pipeline.load_text_column('review')

# Full analysis
(pipeline
 .clean_data(strategy='drop')
 .clean_text()
 .analyze_data()
 .analyze_text()
 .analyze_sentiment()
 .extract_entities()
 .extract_keywords(method='tfidf', top_n=15)
 .detect_topics()
 .analyze_complexity())

# Generate report
print(pipeline.generate_report())

# Export
pipeline.export_results(format='csv', output_dir='results')
pipeline.create_visualizations(output_dir='results')
```

## Real-World Use Cases

### Use Case 1: Customer Feedback Analysis

**Scenario:** Analyze product reviews to understand sentiment and common complaints.
```python
pipeline = UnifiedPipeline()
pipeline.load_structured_data('product_reviews.csv')
pipeline.load_text_column('review_text')

# Analyze
pipeline.analyze_sentiment()
pipeline.extract_keywords(method='tfidf')
pipeline.detect_topics()

# Correlate sentiment with ratings
pipeline.correlate_sentiment_with_column('star_rating')

# Visualize
pipeline.create_visualizations('product_analysis')
```

### Use Case 2: Survey Response Analysis

**Scenario:** Analyze open-ended survey responses with demographic data.
```bash
python cli.py \
  --data-file survey_responses.csv \
  --text-column open_response \
  --correlate age_group \
  --sentiment \
  --topics \
  --visualize
```

### Use Case 3: Social Media Analytics

**Scenario:** Analyze posts with engagement metrics.
```python
pipeline = UnifiedPipeline()
pipeline.load_structured_data('social_posts.csv')
pipeline.load_text_column('post_content')

# Analyze
pipeline.analyze_sentiment()
pipeline.extract_entities()  # Find mentioned brands, people
pipeline.extract_keywords()

# Correlate engagement
pipeline.correlate_sentiment_with_column('likes')
pipeline.correlate_data_with_text_length('shares')
```