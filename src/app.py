import streamlit as st
import json
from src.components.research_agent import ResearchAgent
import time

# Page config
st.set_page_config(
    page_title="CiteSight - Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .research-log {
        font-size: 0.8em;
        color: #666;
    }
    .citation {
        font-style: italic;
        color: #444;
    }
    .key-finding {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #0d47a1;
        white-space: pre-line;
        line-height: 1.5;
    }
    .agreement {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #1b5e20;
        white-space: pre-line;
        line-height: 1.5;
    }
    .contradiction {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #b71c1c;
        white-space: pre-line;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'research_agent' not in st.session_state:
    st.session_state.research_agent = ResearchAgent()
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# Title and description
st.title("🔍 CiteSight Research Assistant")
st.markdown("""
    Enter your research question below, and CiteSight will:
    1. Search for relevant sources
    2. Analyze and summarize the content
    3. Cross-validate information
    4. Generate a cited report
""")

# Input section
question = st.text_area("Enter your research question:", height=100)

# Research button
if st.button("Start Research"):
    if not question:
        st.error("Please enter a research question.")
    else:
        try:
            # Reset state
            st.session_state.research_complete = False
            st.session_state.current_report = None
            
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Start research
            status_text.text("Starting research...")
            progress_bar.progress(10)
            
            # Conduct research
            report = st.session_state.research_agent.research(question)
            
            # Update progress
            progress_bar.progress(100)
            status_text.text("Research complete!")
            
            # Store results
            st.session_state.current_report = report
            st.session_state.research_complete = True
            
            # Rerun to update display
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display results if research is complete
if st.session_state.research_complete and st.session_state.current_report:
    report = st.session_state.current_report
    
    # Check for errors
    if "error" in report:
        st.error(f"Research encountered an error: {report['error']}")
        st.write("Research Log:")
        st.json(report["research_log"])
    else:
        # Display summaries
        st.header("Research Results")
        
        # Sources
        st.subheader("Sources")
        for source in report["sources"]:
            st.markdown(f"- [{source['title']}]({source['url']})")
        
        # Summaries
        st.subheader("Key Findings")
        for i, summary in enumerate(report["summaries"]):
            try:
                # Try to parse the JSON content
                summary_data = json.loads(summary["summary"])
                
                # Skip if summary is empty or contains no meaningful content
                if not summary_data.get("summary") and not summary_data.get("key_points") and not summary_data.get("quotes"):
                    continue
                    
                with st.expander(f"Summary {i+1}"):
                    # Display formatted summary
                    st.markdown("### Summary")
                    st.markdown(summary_data.get("summary", ""))
                    
                    if summary_data.get("key_points"):
                        st.markdown("### Key Points")
                        for point in summary_data["key_points"]:
                            st.markdown(f"- {point}")
                    
                    if summary_data.get("quotes"):
                        st.markdown("### Notable Quotes")
                        for quote in summary_data["quotes"]:
                            st.markdown(f"> {quote}")
                    
                    st.markdown("### Confidence Level")
                    st.info(f"Confidence: {summary_data.get('confidence_level', 'Not specified')}")
                    
                    # Option to view raw JSON
                    if st.checkbox(f"View raw JSON for Summary {i+1}", key=f"raw_json_{i}"):
                        st.json(summary["summary"])
            except:
                # Skip if JSON parsing fails
                continue
        
        # Cross-validation
        st.subheader("Cross-Validation Analysis")
        try:
            # Try to parse the cross-validation JSON
            cross_val = json.loads(report["cross_validation"]["cross_validation"])
            
            # Agreements
            if cross_val.get("agreements"):
                st.markdown("### Points of Agreement")
                points_list = "\n".join([f"✓ {agreement}" for agreement in cross_val["agreements"]])
                st.markdown(f"""
                <div class="agreement">
                    {points_list}
                </div>
                """, unsafe_allow_html=True)
            
            # Contradictions
            if cross_val.get("contradictions"):
                st.markdown("### Points of Contradiction")
                points_list = "\n".join([f"⚠️ {contradiction}" for contradiction in cross_val["contradictions"]])
                st.markdown(f"""
                <div class="contradiction">
                    {points_list}
                </div>
                """, unsafe_allow_html=True)
            
            # Unique points
            if cross_val.get("unique_points"):
                st.markdown("### Unique Information")
                points_list = "\n".join([f"🔍 {point}" for point in cross_val["unique_points"]])
                st.markdown(f"""
                <div class="key-finding">
                    {points_list}
                </div>
                """, unsafe_allow_html=True)
            
            # Overall confidence
            st.markdown("### Overall Confidence Assessment")
            st.info(cross_val.get("confidence", "Not specified"))
            
            # Option to view raw cross-validation JSON
            if st.checkbox("View raw cross-validation JSON"):
                st.json(report["cross_validation"])
        except:
            # Fallback to raw text if JSON parsing fails
            st.write(report["cross_validation"]["cross_validation"])
        
        # Research log
        with st.expander("View Research Log"):
            st.json(report["research_log"])
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Download Report (JSON)",
                data=json.dumps(report, indent=2),
                file_name="research_report.json",
                mime="application/json"
            )
        
        with col2:
            # Create a readable text version of the report
            txt_content = f"""CiteSight Research Report
            
Research Question:
{question}

Sources:
{chr(10).join([f"- {source['title']}: {source['url']}" for source in report['sources']])}

Key Findings:
"""
            # Add summaries
            for i, summary in enumerate(report["summaries"]):
                try:
                    summary_data = json.loads(summary["summary"])
                    if summary_data.get("summary") or summary_data.get("key_points") or summary_data.get("quotes"):
                        txt_content += f"\nSummary {i+1}:\n"
                        txt_content += f"Summary: {summary_data.get('summary', '')}\n"
                        if summary_data.get("key_points"):
                            txt_content += "\nKey Points:\n"
                            txt_content += "\n".join([f"- {point}" for point in summary_data["key_points"]])
                        if summary_data.get("quotes"):
                            txt_content += "\n\nNotable Quotes:\n"
                            txt_content += "\n".join([f"> {quote}" for quote in summary_data["quotes"]])
                        txt_content += f"\nConfidence Level: {summary_data.get('confidence_level', 'Not specified')}\n"
                except:
                    continue

            # Add cross-validation
            try:
                cross_val = json.loads(report["cross_validation"]["cross_validation"])
                txt_content += "\n\nCross-Validation Analysis:\n"
                
                if cross_val.get("agreements"):
                    txt_content += "\nPoints of Agreement:\n"
                    txt_content += "\n".join([f"✓ {point}" for point in cross_val["agreements"]])
                
                if cross_val.get("contradictions"):
                    txt_content += "\n\nPoints of Contradiction:\n"
                    txt_content += "\n".join([f"⚠️ {point}" for point in cross_val["contradictions"]])
                
                if cross_val.get("unique_points"):
                    txt_content += "\n\nUnique Information:\n"
                    txt_content += "\n".join([f"🔍 {point}" for point in cross_val["unique_points"]])
                
                txt_content += f"\n\nOverall Confidence: {cross_val.get('confidence', 'Not specified')}"
            except:
                txt_content += "\nCross-validation data not available"

            st.download_button(
                label="Download Report (TXT)",
                data=txt_content,
                file_name="research_report.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by CiteSight") 