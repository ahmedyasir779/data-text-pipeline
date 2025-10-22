"""
About page - Information about the platform
"""

import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About This Platform")

st.markdown("""
## 🔬 Data & Text Analytics Platform

A unified pipeline for processing structured data and text with advanced NLP capabilities.

### ✨ Features

#### Data Processing
- 📊 Multi-format support (CSV, Excel, JSON)
- 🧹 Intelligent data cleaning
- 📈 Statistical analysis
- 📉 Correlation analysis

#### Text Processing
- 😊 **Sentiment Analysis** - Detect emotional tone (positive, neutral, negative)
- 🏷️ **Named Entity Recognition** - Extract people, organizations, locations
- 🔑 **Keyword Extraction** - Find important terms using RAKE or TF-IDF
- 📑 **Topic Detection** - Automatically categorize content
- 📝 **Text Statistics** - Word counts, unique words, averages

#### Performance
- ⚡ Smart caching (3-10x faster on repeated analyses)
- 📊 Real-time progress tracking
- 💾 Multiple export formats

### 🛠️ Technology Stack

- **Backend:** Python 3.9+
- **Web Framework:** Streamlit
- **Data Processing:** pandas, numpy
- **NLP:** spaCy, NLTK, TextBlob
- **ML:** scikit-learn
- **Visualization:** matplotlib, seaborn
- **Deployment:** Docker, Render

### 📊 Performance

- 10x faster with caching enabled
- Processes 1000+ rows in seconds
- Sub-second sentiment analysis
- Real-time entity extraction

### 🐳 Docker

Pull the Docker image:
```bash
docker pull deeali779/data-text-pipeline:latest
```

### 👨‍💻 Developer

**Ahmed Yasir**
- GitHub: [@ahmedyasir779](https://github.com/ahmedyasir779)
- LinkedIn: [Ahmed Yasir](https://linkedin.com/in/ahmed-yasir-907561206)
- Docker Hub: [@deeali779](https://hub.docker.com/r/deeali779/data-text-pipeline)

### 📄 License

MIT License - Open source and free to use

### 🔗 Links

- [Source Code](https://github.com/ahmedyasir779/data-text-pipeline)
- [Documentation](https://github.com/ahmedyasir779/data-text-pipeline#readme)
- [Docker Hub](https://hub.docker.com/r/deeali779/data-text-pipeline)
- [Report Issues](https://github.com/ahmedyasir779/data-text-pipeline/issues)

### 📅 Version

- Version 1.0.0

---

Made with ❤️ and Python
""")

# Statistics
st.markdown("---")
st.markdown("## 📈 Project Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Lines of Code", "2,500+")

with col2:
    st.metric("Unit Tests", "32")

with col3:
    st.metric("Test Coverage", "75%")

with col4:
    st.metric("Dependencies", "15")