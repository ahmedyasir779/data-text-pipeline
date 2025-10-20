# Testing Guide

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_unified_pipeline.py -v
```

### Run specific test:
```bash
pytest tests/test_unified_pipeline.py::TestUnifiedPipeline::test_initialization -v
```

## Test Structure
```
tests/
├── conftest.py              # Fixtures and configuration
├── test_unified_pipeline.py # Pipeline tests
├── test_cache_manager.py    # Cache tests
└── test_advanced_nlp.py     # NLP tests
```

## Test Coverage

Current coverage: XX%

Target: 80%+

## Writing New Tests

### Test naming:
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example:
```python
def test_my_feature(sample_csv_path):
    pipeline = UnifiedPipeline()
    pipeline.load_structured_data(sample_csv_path)
    
    assert pipeline.data_df is not None
```

## Fixtures

See `conftest.py` for available fixtures:
- `sample_csv_path` - Temporary CSV file
- `sample_dataframe` - Sample DataFrame
- `sample_texts` - Sample text data
- `cache_dir` - Temporary cache directory

## Continuous Integration

Tests run automatically on:
- Every push to dev/main
- Pull requests
- Before deployment