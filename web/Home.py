import streamlit as st
from PIL import Image


def main():
    # Set page configuration
    st.set_page_config(
        page_title="K-RealEstate AI Assistant",
        page_icon="🏠",
        layout="wide"
    )

    # Custom CSS to ensure consistent spacing and styling
    st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .element-container {
            margin-bottom: 1rem;
        }
        .stExpander {
            border: none !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12) !important;
            margin-bottom: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        st.page_link("Home.py", label="Home", icon="🌟")
        # st.page_link("pages/search.py", label="Property Search", icon="🔍")
        # st.page_link("pages/analysis.py", label="Market Analysis", icon="📊")
        # st.page_link("pages/about.py", label="About", icon="ℹ️")

        st.markdown("---")
        with st.expander("Contact"):
            st.markdown("📧 support@example.com")
            st.markdown("📱 +82 10-1234-5678")

    # Main content
    st.title("K-RealEstate AI Assistant")
    st.subheader("Intelligent Korean Real Estate Data Analysis Platform")
    st.markdown("---")

    # Our Mission - Full width
    with st.expander("🎯 Our Mission", expanded=True):
        st.markdown("""
        Transforming Korean real estate data into actionable insights through AI.

        We aim to provide accurate, real-time property information and market analysis
        using cutting-edge AI technology.
        """)

    # Technology Stack and Data Sources in two columns
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🛠 Technology Stack", expanded=True):
            st.markdown("""
            - Crawl4AI
            - OpenAI API
            - PandasAI
            - Streamlit
            """)

    with col2:
        with st.expander("📊 Data Sources", expanded=True):
            st.markdown("""
            - Naver Real Estate
            - Public Property Records
            - Market Analysis Reports
            - Regional Development Plans
            """)

    # How It Works section with consistent styling
    st.markdown("---")
    st.markdown("### How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("1. Data Collection", expanded=True):
            st.markdown("""
            - Automated crawling system
            - Real-time data updates
            - Multiple source integration
            """)

    with col2:
        with st.expander("2. AI Processing", expanded=True):
            st.markdown("""
            - Natural language processing
            - Data structuring
            - Pattern recognition
            """)

    with col3:
        with st.expander("3. User Interaction", expanded=True):
            st.markdown("""
            - Intuitive query interface
            - Custom search filters
            - Interactive visualizations
            """)

    # Call-to-action with better spacing
    st.markdown("---")
    st.markdown("### Ready to explore Korean real estate data?")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.button("Start Searching 🔍", use_container_width=True, type="primary")


if __name__ == "__main__":
    main()