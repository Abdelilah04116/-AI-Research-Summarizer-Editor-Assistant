"""
Streamlit frontend for the Research Assistant
"""
import streamlit as st
import requests
import time
import os
from typing import Dict, Any, List, Optional


# Constants
API_URL = os.environ.get("API_URL", "http://backend:8000")
POLLING_INTERVAL = 3  # seconds


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Research Assistant",
        page_icon="🔍",
        layout="wide",
    )
    
    st.title("🔍 AI Research Assistant")
    st.subheader("Powered by CrewAI Multi-Agent System")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password")
        st.caption("Your API key is used only for this session and not stored.")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This research assistant uses a team of AI agents to:
        1. Research topics in-depth
        2. Summarize findings
        3. Create polished final reports
        """)
    
    # Main content
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.header("Research Request")
        with st.form("research_form"):
            topic = st.text_input("Research Topic", placeholder="e.g., Quantum Computing")
            depth = st.select_slider(
                "Research Depth",
                options=["basic", "medium", "comprehensive"],
                value="medium"
            )
            
            focus_areas = st.text_area(
                "Focus Areas (Optional)",
                placeholder="Enter specific areas to focus on, one per line"
            )
            
            submit_button = st.form_submit_button("Start Research")
            
            if submit_button:
                if not api_key:
                    st.error("Please enter your OpenAI API key")
                elif not topic:
                    st.error("Please enter a research topic")
                else:
                    # Parse focus areas
                    focus_areas_list = [area.strip() for area in focus_areas.split("\n") if area.strip()]
                    
                    # Create session state for tracking
                    st.session_state.research_in_progress = True
                    st.session_state.topic = topic
                    
                    # Submit research request
                    with st.spinner("Submitting research request..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/research",
                                json={
                                    "topic": topic,
                                    "depth": depth,
                                    "focus_areas": focus_areas_list
                                },
                                headers={"X-API-Key": api_key}
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.task_id = data["task_id"]
                                st.success("Research request submitted!")
                            else:
                                st.error(f"Error: {response.status_code} - {response.text}")
                                st.session_state.research_in_progress = False
                        
                        except Exception as e:
                            st.error(f"Failed to connect to the API: {str(e)}")
                            st.session_state.research_in_progress = False
    
    with col2:
        st.header("Research Results")
        
        # Check if research is in progress
        if st.session_state.get("research_in_progress", False):
            task_id = st.session_state.get("task_id")
            topic = st.session_state.get("topic")
            
            st.info(f"Researching: {topic}")
            
            progress_placeholder = st.empty()
            results_placeholder = st.empty()
            
            try:
                # Poll for results
                with progress_placeholder:
                    progress_bar = st.progress(0)
                    
                    # Simulated progress since we don't have real-time progress info
                    for percent_complete in range(0, 101, 10):
                        # Check status
                        response = requests.get(f"{API_URL}/research/{task_id}")
                        data = response.json()
                        
                        if data["status"] == "complete":
                            progress_bar.progress(100)
                            
                            with results_placeholder:
                                display_results(data["results"])
                            
                            st.session_state.research_in_progress = False
                            break
                        
                        elif data["status"] == "failed":
                            st.error(f"Research failed: {data.get('error', 'Unknown error')}")
                            st.session_state.research_in_progress = False
                            break
                        
                        # Update progress bar
                        progress_bar.progress(percent_complete)
                        time.sleep(POLLING_INTERVAL)
                
            except Exception as e:
                st.error(f"Error retrieving results: {str(e)}")
                st.session_state.research_in_progress = False
        
        else:
            st.info("Submit a research topic to start")


def display_results(results: Dict[str, Any]):
    """Display research results in tabs"""
    st.success("Research completed!")
    
    tab1, tab2, tab3 = st.tabs(["Final Report", "Summary", "Raw Research"])
    
    with tab1:
        st.markdown("## Final Report")
        st.markdown(results["final_report"])
        
        # Download button for report
        st.download_button(
            label="Download Report",
            data=results["final_report"],
            file_name=f"{results['topic'].replace(' ', '_')}_report.md",
            mime="text/markdown"
        )
    
    with tab2:
        st.markdown("## Summary")
        st.markdown(results["summary"])
    
    with tab3:
        st.markdown("## Raw Research Data")
        st.markdown(results["research_data"]["raw_research"])


if __name__ == "__main__":
    main()
