# 🔗 Unified Data + Text Pipeline

Combine structured data processing with NLP text analysis in one seamless workflow.

**Integration of:**
- `data-processor` - Structured data handling
- `text-processor` - NLP text analysis

## ✨ Features

### 🔄 Unified Workflow
- Load structured data (CSV, Excel, JSON)
- Extract text from data columns OR load separate text files
- Process both in a single pipeline
- Analyze relationships between data and text

### 📊 Data Processing
- Clean missing values
- Remove duplicates
- Statistical analysis
- Multiple file format support

### 📝 Text Processing
- Clean text (URLs, emails, special chars)
- Tokenization
- Word frequency analysis
- Basic NLP statistics

### 🔗 Integration Features
- Correlate numeric data with text length
- Unified reporting
- Combined insights

## 🚀 Quick Start
```bash
# Install
git clone https://github.com/ahmedyasir779/data-text-pipeline.git
cd data-text-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python cli.py --data-file data.csv --text-column reviews --all
```

## 📖 Usage Examples

### Example 1: Customer Reviews Analysis
```bash
python cli.py \
  --data-file customer_reviews.csv \
  --text-column review \
  --correlate rating \
  --all
```

**Output:**
- Statistical analysis of ratings, prices, sales
- Text analysis of reviews
- Correlation: Do longer reviews correlate with higher ratings?

### Example 2: Survey Data
```bash
python cli.py \
  --data-file survey.csv \
  --text-column feedback \
  --clean \
  --all
```

### Example 3: Separate Text File
```bash
python cli.py \
  --data-file sales_data.csv \
  --text-file customer_feedback.txt \
  --all
```

## 🔧 CLI Options
```
--data-file, -d      Input data file (CSV/Excel/JSON)
--text-column, -t    Column containing text
--text-file          Separate text file
--clean, -c          Clean data and text
--correlate          Correlate column with text length
--all, -a            Run complete analysis
--output, -o         Output file path
```

## 📊 What It Analyzes

### Structured Data:
- Mean, median, std, min, max for numeric columns
- Missing value handling
- Duplicate detection

### Text Data:
- Total words
- Unique words
- Word frequency
- Average words per entry

### Combined:
- Correlation between numeric values and text length
- Example: Rating vs Review Length

## 🎯 Use Cases

1. **E-commerce:** Product ratings + customer reviews
2. **Surveys:** Demographics + open-ended responses
3. **Social Media:** Engagement metrics + post content
4. **Support Tickets:** Priority scores + ticket descriptions
5. **Research:** Quantitative data + qualitative feedback

## 🗂️ Project Structure
```
data-text-pipeline/
├── unified_pipeline.py    # Core pipeline logic
├── cli.py                 # Command-line interface
├── create_test_data.py    # Test data generator
├── data/                  # Input data
├── output/                # Generated reports
└── tests/                 # Test suite
```

## 📚 Documentation

See individual modules for detailed API documentation.

## 🤝 Related Projects

This integrates:
- [data-processor](https://github.com/ahmedyasir779/data-processor) v1.0.0
- [text-processor](https://github.com/ahmedyasir779/text-processor) v1.0.0

## 📄 License

MIT License

## 👤 Author

**Ahmed**
- GitHub: [@Yahmedyasir779](https://github.com/ahmedyasir779)
- LinkedIn: [Ahmed Yasir](https://linkedin.com/in/ahmed-yasir-907561206)

---
