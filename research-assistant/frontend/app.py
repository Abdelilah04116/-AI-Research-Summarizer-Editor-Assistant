import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from io import StringIO

# Configuration de la page
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personnalisation CSS
st.markdown("""
<style>
    .main-header {color: #4B8BBE; font-size: 32px;}
    .sub-header {color: #4B8BBE; font-size: 24px;}
    .status-complete {color: green;}
    .status-progress {color: orange;}
    .status-waiting {color: gray;}
    .chat-user {
        background-color: #e6f3ff;
        padding: 10px;
        border-radius: 4px;
        margin: 5px 0 5px 20%;
    }
    .chat-assistant {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 4px;
        margin: 5px 20% 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    openai_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Model", ["GPT-4", "GPT-3.5-Turbo"])
    scholar_key = st.text_input("Google Scholar API Key", type="password")
    pubmed_key = st.text_input("PubMed API Key", type="password")
    
    st.header("Navigation")
    
    st.button("New Research")
    st.button("Research History")
    st.button("Feedback Analytics")
    
    st.header("About")
    st.write("Uses AI agents for research, summarization, and editing.")

# Main Content
st.markdown("<h1 class='main-header'>Multi-Agent Research Assistant</h1>", unsafe_allow_html=True)

# Research Status
st.markdown("<h2>Research Status</h2>", unsafe_allow_html=True)
st.markdown("<strong>Status:</strong> In Progress", unsafe_allow_html=True)

status_cols = st.columns(3)
with status_cols[0]:
    st.markdown("<h3>✅ Researcher</h3>", unsafe_allow_html=True)
    st.markdown("<p class='status-complete'>Complete</p>", unsafe_allow_html=True)
with status_cols[1]:
    st.markdown("<h3>⏳ Summarizer</h3>", unsafe_allow_html=True)
    st.markdown("<p class='status-progress'>In Progress</p>", unsafe_allow_html=True)
with status_cols[2]:
    st.markdown("<h3>⏱️ Editor</h3>", unsafe_allow_html=True)
    st.markdown("<p class='status-waiting'>Waiting</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Final Report", "Summary", "Visualizations", "External Sources", "Research Data", "Process Log"])

with tab1:
    st.header("Final Report")
    st.write("The final report will appear here when complete.")

with tab2:
    st.header("Summary")
    st.write("Research summary will appear here.")

with tab3:
    st.header("Visualizations")
    
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(["Word Frequency", "Word Cloud", "Topic Clusters", "Sentiment Analysis"])
    
    with viz_tab1:
        # Sample data for word frequency
        words = ["research", "data", "analysis", "ai", "results", "method", "paper"]
        frequencies = [24, 18, 15, 12, 10, 8, 5]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(words, frequencies)
        ax.set_title("Word Frequency")
        ax.set_xlabel("Words")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    
    with viz_tab2:
        # Sample data for word cloud
        text = "research data analysis AI results method paper research AI data analysis research"
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    
    with viz_tab3:
        # Sample data for topic clusters
        df = pd.DataFrame({
            'topic': ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4'],
            'count': [35, 27, 21, 17],
            'keyword1': ['research', 'data', 'method', 'results'],
            'keyword2': ['paper', 'analysis', 'approach', 'findings']
        })
        
        fig = px.scatter(df, x='count', y='topic', size='count', 
                         text='topic', hover_data=['keyword1', 'keyword2'],
                         title="Topic Clusters")
        st.plotly_chart(fig)
    
    with viz_tab4:
        # Sample data for sentiment analysis
        sentiments = ['Positive', 'Neutral', 'Negative']
        values = [65, 25, 10]
        
        fig = px.pie(values=values, names=sentiments, title="Sentiment Analysis")
        st.plotly_chart(fig)

with tab4:
    st.header("External Sources")
    st.write("List of external sources consulted during research.")
    sources = [
        {"title": "Sample Paper 1", "authors": "Smith et al.", "year": 2023},
        {"title": "Sample Paper 2", "authors": "Johnson et al.", "year": 2022},
        {"title": "Sample Paper 3", "authors": "Williams et al.", "year": 2023}
    ]
    st.table(pd.DataFrame(sources))

with tab5:
    st.header("Research Data")
    st.write("Raw research data will appear here.")

with tab6:
    st.header("Process Log")
    st.write("Detailed log of the research process.")

# Chat Section
st.markdown("<h3 class='sub-header'>Chat with Research Assistant</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "What are the key findings?"},
        {"role": "assistant", "content": "The research highlights several important findings. Once the summarizer agent completes its work, I can provide you with a comprehensive overview of the key insights discovered during this research project."}
    ]

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-user'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-assistant'>{message['content']}</div>", unsafe_allow_html=True)

chat_input = st.text_input("Ask a question", key="chat_input")
chat_button = st.button("Send")

if chat_button and chat_input:
    st.session_state.messages.append({"role": "user", "content": chat_input})
    # In a real application, you would process the question here
    response = "I'll need to analyze that further. The AI assistant will respond when ready."
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.experimental_rerun()

# Feedback Section
st.markdown("<h3 class='sub-header'>Feedback</h3>", unsafe_allow_html=True)

feedback_type = st.selectbox("Feedback Category", ["Overall Quality", "Accuracy", "Relevance", "Completeness"])
feedback_rating = st.slider("Rating", 1, 5, 4)
feedback_text = st.text_area("Your thoughts...")
feedback_button = st.button("Submit Feedback")

if feedback_button:
    st.success("Thank you for your feedback!")