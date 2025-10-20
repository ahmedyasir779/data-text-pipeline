# Configuration Guide

## Configuration File Format

Supports JSON and YAML formats.

### JSON Example
```json
{
  "pipeline": {
    "use_cache": true,
    "clean_strategy": "drop",
    "analyze_sentiment": true,
    "extract_entities": true,
    "extract_keywords": true,
    "keyword_method": "tfidf",
    "detect_topics": true,
    "analyze_complexity": true
  },
  "visualization": {
    "create_dashboard": true,
    "dpi": 300,
    "style": "whitegrid"
  },
  "export": {
    "format": "csv",
    "include_sentiment": true,
    "include_entities": false
  },
  "output": {
    "directory": "output",
    "report_name": "analysis_report.txt"
  }
}
```

### YAML Example
```yaml
pipeline:
  use_cache: true
  clean_strategy: drop
  analyze_sentiment: true
  extract_entities: true
  extract_keywords: true
  keyword_method: tfidf
  detect_topics: true
  analyze_complexity: true

visualization:
  create_dashboard: true
  dpi: 300
  style: whitegrid

export:
  format: csv
  include_sentiment: true
  include_entities: false

output:
  directory: output
  report_name: analysis_report.txt
```

## Configuration Options

### Pipeline Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `use_cache` | boolean | `true` | Enable caching |
| `clean_strategy` | string | `"drop"` | Missing value strategy |
| `analyze_sentiment` | boolean | `false` | Run sentiment analysis |
| `extract_entities` | boolean | `false` | Extract named entities |
| `extract_keywords` | boolean | `false` | Extract keywords |
| `keyword_method` | string | `"tfidf"` | Keyword method (rake/tfidf) |
| `detect_topics` | boolean | `false` | Detect topics |
| `analyze_complexity` | boolean | `false` | Analyze text complexity |

### Visualization Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `create_dashboard` | boolean | `false` | Generate dashboard |
| `dpi` | integer | `300` | Image resolution |
| `style` | string | `"whitegrid"` | Seaborn style |

### Export Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `format` | string | `"csv"` | Export format (csv/json/excel) |
| `include_sentiment` | boolean | `true` | Include sentiment in export |
| `include_entities` | boolean | `false` | Include entities in export |

### Output Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `directory` | string | `"output"` | Output directory |
| `report_name` | string | `"unified_report.txt"` | Report filename |

## Usage

### Load Configuration
```bash
python cli.py --data-file data.csv --text-column text --config my_config.json
```

### Generate Default Configuration
```python
from config_manager import ConfigManager

config = ConfigManager.create_default_config()
ConfigManager.save_config(config, 'default_config.json')
```

## Environment Variables

You can also use environment variables:
```bash
export PIPELINE_CACHE_ENABLED=true
export PIPELINE_OUTPUT_DIR=results
export PIPELINE_LOG_LEVEL=INFO

python cli.py --data-file data.csv --text-column text --all
```