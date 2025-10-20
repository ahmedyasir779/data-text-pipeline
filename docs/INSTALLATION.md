# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/ahmedyasir779/data-text-pipeline.git
cd data-text-pipeline
```

### 2. Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLP Models
```bash
# spaCy model
python -m spacy download en_core_web_sm

# TextBlob corpora
python -m textblob.download_corpora
```

### 5. Verify Installation
```bash
# Run tests
pytest tests/ -v

# Run example
python cli.py --help
```

## Troubleshooting

### Issue: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Issue: Permission denied
```bash
pip install --user -r requirements.txt
```

### Issue: Module not found
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Optional Dependencies

### For development:
```bash
pip install pytest pytest-cov pytest-mock
```

### For visualization enhancements:
```bash
pip install plotly kaleido
```

## Docker Installation (Alternative)
```bash
# Build image
docker build -t data-text-pipeline .

# Run container
docker run -v $(pwd)/data:/app/data data-text-pipeline --data-file /app/data/sample.csv --all
```