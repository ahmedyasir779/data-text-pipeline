# Architecture Documentation

## System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
├─────────────────────────────────────────────────────────────┤
│  CLI (cli.py)                                               │
│  • Command-line arguments                                   │
│  • Configuration file support                               │
│  • Interactive mode                                         │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│              UNIFIED PIPELINE CORE                          │
│         (unified_pipeline.py)                               │
├─────────────────────────────────────────────────────────────┤
│  Orchestration Layer:                                       │
│  • Method chaining                                          │
│  • State management                                         │
│  • Result aggregation                                       │
│  • Error handling                                           │
└─┬───────┬───────────┬───────────┬───────────┬──────────────┘
  │       │           │           │           │
  │   ┌───▼────┐  ┌───▼────┐  ┌──▼──────┐  ┌▼──────────┐
  │   │ Data   │  │ Text   │  │Advanced │  │Visualization│
  │   │Cleaning│  │Cleaning│  │  NLP    │  │  Engine    │
  │   └────────┘  └────────┘  └─────────┘  └────────────┘
  │
┌─▼──────────────────────────────────────────────────────────┐
│              SUPPORT SERVICES                               │
├────────────────────────────────────────────────────────────┤
│  • Cache Manager (cache_manager.py)                        │
│  • Progress Tracker (progress_tracker.py)                  │
│  • Config Manager (config_manager.py)                      │
│  • Logger (logging system)                                 │
└────────────────────────────────────────────────────────────┘
```

## Data Flow
```
Input File → Load → Cache Check → Clean → Analyze → Visualize → Export
             │         │            │       │          │          │
             └─────────┴────────────┴───────┴──────────┴──────────┘
                              Cache Storage
```
## Module Responsibilities
```
Core Module: unified_pipeline.py
Responsibilities:

Orchestrate all processing steps
Manage pipeline state
Aggregate results
Handle errors gracefully
```
## Key Methods:
```
load_structured_data()  # Load CSV/Excel/JSON
load_text_column()      # Extract text from data
clean_data()            # Clean structured data
analyze_data()          # Statistical analysis
analyze_sentiment()     # Sentiment analysis
extract_entities()      # NER
create_visualizations() # Generate charts
export_results()        # Export to file
```

### NLP Module: `advanced_nlp.py`

**Responsibilities:**
- Named Entity Recognition
- Keyword extraction
- Topic detection
- Readability analysis

**Technologies:**
- spaCy (entity recognition)
- RAKE-NLTK (keyword extraction)
- sklearn (TF-IDF)
- Custom algorithms (readability)

### Cache Module: `cache_manager.py`

**Responsibilities:**
- Store expensive computations
- Generate cache keys (MD5 hashing)
- Manage cache lifecycle
- Track cache statistics

**Storage Structure:**
```
.cache/
├── data/       # Loaded datasets
├── analysis/   # Statistical results
└── nlp/        # NLP results

Progress Module: progress_tracker.py
Responsibilities:

Display progress bars
Show time estimates
Track operation timing

Features:

tqdm integration
Nested progress bars
Time estimation

Config Module: config_manager.py
Responsibilities:

Load JSON/YAML configs
Validate configuration
Provide defaults

Processing Pipeline
1. Data Loading Phase
pipeline.load_structured_data('data.csv')
# ↓
# - Check cache
# - Load file (pandas)
# - Store in cache
# - Return DataFrame


2. Text Loading Phase
pipeline.load_text_column('review')
# ↓
# - Extract column
# - Drop null values
# - Store as list

3. Cleaning Phase
pipeline.clean_data().clean_text()
# ↓
# Data: Remove nulls, duplicates, outliers
# Text: Remove HTML, URLs, normalize

4. Analysis Phase
pipeline.analyze_data().analyze_text().analyze_sentiment()
# ↓
# - Check cache for each operation
# - Compute if not cached
# - Store results
# - Update cache

5. NLP Phase
pipeline.extract_entities().extract_keywords().detect_topics()
# ↓
# - spaCy NER
# - RAKE/TF-IDF keywords
# - Topic clustering

6. Visualization Phase
pipeline.create_visualizations()
# ↓
# - Generate 6-panel dashboard
# - Save to PNG (300 DPI)

7. Export Phase
pipeline.export_results(format='csv')
# ↓
# - Add sentiment/entities to data
# - Export to chosen format
