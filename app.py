import streamlit as st
import pandas as pd
import os
from pathlib import Path
import base64
from io import BytesIO
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from unified_pipeline import UnifiedPipeline

# Page configuration
st.set_page_config(
    page_title="Data & Text Analytics",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def get_download_link(df, filename, file_label):
    """Generate download link for DataFrame"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'


def display_sentiment_results(results):
    """Display sentiment analysis results"""
    st.markdown('<p class="sub-header">📊 Sentiment Analysis</p>', unsafe_allow_html=True)
    
    sentiment = results['sentiment']
    
    # Metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Positive Reviews", sentiment['positive_count'], 
                  f"{sentiment['positive_count']/sentiment['total']*100:.1f}%")
    
    with col2:
        st.metric("Neutral Reviews", sentiment['neutral_count'],
                  f"{sentiment['neutral_count']/sentiment['total']*100:.1f}%")
    
    with col3:
        st.metric("Negative Reviews", sentiment['negative_count'],
                  f"{sentiment['negative_count']/sentiment['total']*100:.1f}%")
    
    with col4:
        st.metric("Avg Polarity", f"{sentiment['avg_polarity']:.3f}")
    
    # Sentiment distribution
    sentiment_df = pd.DataFrame({
        'Category': ['Positive', 'Neutral', 'Negative'],
        'Count': [sentiment['positive_count'], sentiment['neutral_count'], sentiment['negative_count']]
    })
    
    st.bar_chart(sentiment_df.set_index('Category'))


def display_entity_results(results):
    """Display entity extraction results"""
    st.markdown('<p class="sub-header">🏷️ Named Entities</p>', unsafe_allow_html=True)
    
    entities = results.get('entities', {})
    
    if not entities:
        st.info("No entities found. Run entity extraction first.")
        return
    
    # Display entities by type
    cols = st.columns(3)
    
    for idx, (entity_type, data) in enumerate(entities.items()):
        with cols[idx % 3]:
            st.markdown(f"**{entity_type}**")
            st.metric("Total Mentions", data['total'])
            st.metric("Unique Entities", data['unique'])
            
            if data.get('entities'):
                with st.expander(f"View {entity_type} entities"):
                    # Show top 10
                    for entity, count in list(data['entities'].items())[:10]:
                        st.write(f"• {entity}: {count} mentions")


def display_keyword_results(results):
    """Display keyword extraction results"""
    st.markdown('<p class="sub-header">🔑 Top Keywords</p>', unsafe_allow_html=True)
    
    keywords = results.get('keywords', [])
    
    if not keywords:
        st.info("No keywords found. Run keyword extraction first.")
        return
    
    # Create DataFrame
    keyword_df = pd.DataFrame(keywords, columns=['Keyword', 'Score'])
    keyword_df['Score'] = keyword_df['Score'].round(3)
    
    # Display as chart
    st.bar_chart(keyword_df.set_index('Keyword')['Score'])
    
    # Display as table
    with st.expander("View keyword details"):
        st.dataframe(keyword_df)


def display_topic_results(results):
    """Display topic detection results"""
    st.markdown('<p class="sub-header">📑 Detected Topics</p>', unsafe_allow_html=True)
    
    topics = results.get('topics', {})
    
    if not topics:
        st.info("No topics found. Run topic detection first.")
        return
    
    for topic_name, keywords in topics.items():
        with st.expander(f"🏷️ {topic_name}"):
            # Handle both list of strings and list of tuples
            if keywords and isinstance(keywords[0], tuple):
                # It's a list of (keyword, score) tuples
                keyword_list = [kw for kw, score in keywords]
                st.write("**Keywords:**", ", ".join(keyword_list))
                
                # Show scores
                with st.expander("View keyword scores"):
                    for kw, score in keywords:
                        st.write(f"• {kw}: {score:.3f}")
            else:
                # It's a list of strings
                st.write("**Keywords:**", ", ".join(keywords))


def display_text_stats(results):
    """Display text statistics"""
    st.markdown('<p class="sub-header">📝 Text Statistics</p>', unsafe_allow_html=True)
    
    stats = results.get('text_statistics', {})
    
    if not stats:
        st.info("No text statistics available.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", stats.get('total_entries', 0))
    
    with col2:
        st.metric("Total Words", stats.get('total_words', 0))
    
    with col3:
        st.metric("Unique Words", stats.get('unique_words', 0))
    
    with col4:
        st.metric("Avg Words/Entry", stats.get('avg_words_per_entry', 0))


def display_data_stats(results):
    """Display data statistics"""
    st.markdown('<p class="sub-header">📊 Data Statistics</p>', unsafe_allow_html=True)
    
    stats = results.get('data_statistics', {})
    
    if not stats:
        st.info("No data statistics available.")
        return
    
    # Display statistics for each numeric column
    for column, col_stats in stats.items():
        with st.expander(f"📈 {column}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Mean", f"{col_stats.get('mean', 0):.2f}")
            with col2:
                st.metric("Median", f"{col_stats.get('median', 0):.2f}")
            with col3:
                st.metric("Std Dev", f"{col_stats.get('std', 0):.2f}")
            with col4:
                st.metric("Min/Max", f"{col_stats.get('min', 0):.1f} / {col_stats.get('max', 0):.1f}")


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🔬 Data & Text Analytics Platform</h1>', unsafe_allow_html=True)
    st.markdown("**Unified pipeline for structured data and text processing with advanced NLP**")
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Data File",
        type=['csv', 'xlsx', 'json'],
        help="Upload CSV, Excel, or JSON file"
    )
    
    if not uploaded_file:
        st.info("👈 Upload a data file to get started")
        
        # Show example
        with st.expander("📖 How to use"):
            st.markdown("""
            ### Quick Start Guide
            
            1. **Upload File** - Upload CSV, Excel, or JSON file using sidebar
            2. **Select Text Column** - Choose which column contains text data
            3. **Choose Analysis** - Select which analyses to run
            4. **Process** - Click "Run Analysis" button
            5. **View Results** - See beautiful visualizations and insights
            6. **Download** - Export results as CSV or report
            
            ### Features
            
            - 📊 **Data Analysis** - Statistical analysis of numeric columns
            - 😊 **Sentiment Analysis** - Detect positive, neutral, negative sentiment
            - 🏷️ **Entity Recognition** - Extract people, organizations, locations
            - 🔑 **Keyword Extraction** - Find important keywords (RAKE or TF-IDF)
            - 📑 **Topic Detection** - Automatically categorize content
            - 📝 **Text Statistics** - Word counts, unique words, averages
            
            ### Example Use Cases
            
            - Customer review analysis
            - Survey response processing
            - Social media sentiment tracking
            - Product feedback analysis
            - Support ticket categorization
            """)
        
        return
    
    # Save uploaded file temporarily
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    file_path = temp_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✓ Loaded: {uploaded_file.name}")
    
    # Load and preview data
    try:
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path)
        
        st.markdown("### 📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        st.caption(f"Showing 10 of {len(df)} rows")
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return
    
    # Configuration options
    st.sidebar.markdown("---")
    st.sidebar.subheader("Text Column")
    
    text_column = st.sidebar.selectbox(
        "Select text column",
        options=df.columns.tolist(),
        help="Column containing text data to analyze"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Analysis Options")
    
    run_data_analysis = st.sidebar.checkbox("📊 Data Analysis", value=True)
    run_text_stats = st.sidebar.checkbox("📝 Text Statistics", value=True)
    run_sentiment = st.sidebar.checkbox("😊 Sentiment Analysis", value=True)
    run_entities = st.sidebar.checkbox("🏷️ Entity Recognition", value=False)
    run_keywords = st.sidebar.checkbox("🔑 Keyword Extraction", value=False)
    run_topics = st.sidebar.checkbox("📑 Topic Detection", value=False)
    
    if run_keywords:
        keyword_method = st.sidebar.radio(
            "Keyword Method",
            options=['rake', 'tfidf'],
            help="RAKE: rule-based, TF-IDF: statistical"
        )
    
    st.sidebar.markdown("---")
    use_cache = st.sidebar.checkbox("⚡ Use Caching", value=True, help="Speed up repeated analyses")
    
    # Run button
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        
        with st.spinner("Processing... This may take a moment"):
            
            try:
                # Initialize pipeline
                pipeline = UnifiedPipeline(use_cache=use_cache)
                
                # Progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Load data
                status_text.text("Loading data...")
                progress_bar.progress(10)
                pipeline.load_structured_data(str(file_path))
                
                # Load text column
                status_text.text("Loading text data...")
                progress_bar.progress(20)
                pipeline.load_text_column(text_column)
                
                # Clean data
                status_text.text("Cleaning data...")
                progress_bar.progress(30)
                pipeline.clean_data()
                
                # Run selected analyses
                current_progress = 40
                
                if run_data_analysis:
                    status_text.text("Analyzing data...")
                    progress_bar.progress(current_progress)
                    pipeline.analyze_data()
                    current_progress += 10
                
                if run_text_stats:
                    status_text.text("Analyzing text...")
                    progress_bar.progress(current_progress)
                    pipeline.analyze_text()
                    current_progress += 10
                
                if run_sentiment:
                    status_text.text("Analyzing sentiment...")
                    progress_bar.progress(current_progress)
                    pipeline.analyze_sentiment()
                    current_progress += 10
                
                if run_entities:
                    status_text.text("Extracting entities...")
                    progress_bar.progress(current_progress)
                    pipeline.extract_entities()
                    current_progress += 10
                
                if run_keywords:
                    status_text.text("Extracting keywords...")
                    progress_bar.progress(current_progress)
                    pipeline.extract_keywords(method=keyword_method)
                    current_progress += 10
                
                if run_topics:
                    status_text.text("Detecting topics...")
                    progress_bar.progress(current_progress)
                    pipeline.detect_topics()
                    current_progress += 10
                
                progress_bar.progress(100)
                status_text.text("Complete!")
                
                # Store results in session state
                st.session_state['results'] = pipeline.results
                st.session_state['pipeline'] = pipeline
                
                st.balloons()
                
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.exception(e)
                return
    
    # Display results
    if 'results' in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Results")
        
        results = st.session_state['results']
        pipeline = st.session_state['pipeline']
        
        # Create tabs for different result types
        tabs = []
        tab_names = []
        
        if 'data_statistics' in results:
            tab_names.append("📊 Data Stats")
        if 'text_statistics' in results:
            tab_names.append("📝 Text Stats")
        if 'sentiment' in results:
            tab_names.append("😊 Sentiment")
        if 'entities' in results:
            tab_names.append("🏷️ Entities")
        if 'keywords' in results:
            tab_names.append("🔑 Keywords")
        if 'topics' in results:
            tab_names.append("📑 Topics")
        
        tabs = st.tabs(tab_names)
        
        tab_idx = 0
        
        if 'data_statistics' in results:
            with tabs[tab_idx]:
                display_data_stats(results)
            tab_idx += 1
        
        if 'text_statistics' in results:
            with tabs[tab_idx]:
                display_text_stats(results)
            tab_idx += 1
        
        if 'sentiment' in results:
            with tabs[tab_idx]:
                display_sentiment_results(results)
            tab_idx += 1
        
        if 'entities' in results:
            with tabs[tab_idx]:
                display_entity_results(results)
            tab_idx += 1
        
        if 'keywords' in results:
            with tabs[tab_idx]:
                display_keyword_results(results)
            tab_idx += 1
        
        if 'topics' in results:
            with tabs[tab_idx]:
                display_topic_results(results)
            tab_idx += 1
        
        # Download section
        st.markdown("---")
        st.markdown("## 💾 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate report
            report = pipeline.generate_report()
            
            st.download_button(
                label="📄 Download Text Report",
                data=report,
                file_name="analysis_report.txt",
                mime="text/plain"
            )
        
        with col2:
            # Export data with sentiment (if available)
            if 'sentiment' in results and pipeline.data_df is not None:
                export_df = pipeline.data_df.copy()
                
                # Add sentiment scores
                sentiments = results['sentiment']['sentiments']
                export_df['sentiment_polarity'] = [s['polarity'] for s in sentiments]
                export_df['sentiment_subjectivity'] = [s['subjectivity'] for s in sentiments]
                
                # Convert to CSV
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="📊 Download CSV with Sentiment",
                    data=csv,
                    file_name="data_with_sentiment.csv",
                    mime="text/csv"
                )


if __name__ == "__main__":
    main()