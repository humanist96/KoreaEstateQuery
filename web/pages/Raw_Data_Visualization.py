import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def set_custom_style():
    st.markdown("""
        <style>
        /* Main containers */
        .stApp {
            background-color: #f8f9fa;
        }

        /* Headers */
        h1 {
            color: #2c3e50;
            font-weight: 600;
        }
        h2 {
            color: #34495e;
            font-weight: 500;
        }
        h3 {
            color: #445566;
            font-weight: 500;
        }

        /* Expander styling */
        .streamlit-expander {
            border: 1px solid #e1e4e8 !important;
            border-radius: 8px !important;
            background-color: white !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            margin-bottom: 1rem !important;
        }

        /* Button styling */
        .stButton > button {
            background-color: #4b6584;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #3c5270;
        }

        /* Primary button */
        .stButton > button[kind="primary"] {
            background-color: #3498db;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #2980b9;
        }

        /* Success message */
        .success {
            background-color: #d4edda;
            color: #155724;
            padding: 0.75rem;
            border-radius: 6px;
            border: 1px solid #c3e6cb;
        }

        /* Warning message */
        .warning {
            background-color: #fff3cd;
            color: #856404;
            padding: 0.75rem;
            border-radius: 6px;
            border: 1px solid #ffeeba;
        }

        /* DataFrames */
        .dataframe {
            background-color: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }

        /* Selectbox and Multiselect base */
        .stSelectbox [data-baseweb="select"] {
            background-color: #f8f9fa !important;
        }
        .stMultiSelect [data-baseweb="select"] {
            background-color: #f8f9fa !important;
        }

        /* Multiselect pills styling */
        .stMultiSelect span[data-baseweb="tag"] {
            background-color: #e3eaef !important;
            color: #2c3e50 !important;
            border-radius: 4px !important;
            padding: 4px 8px !important;
            font-size: 0.9em !important;
        }

        /* Close button in multiselect pills */
        .stMultiSelect span[data-baseweb="tag"] span[role="button"] {
            color: #34495e !important;
            padding-left: 4px !important;
        }

        /* File uploader */
        .stUploadedFile {
            background-color: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 1rem;
        }

        /* Charts container */
        .chart-container {
            background-color: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Select box text color */
        .stSelectbox div[data-baseweb="select"] span {
            color: #2c3e50 !important;
        }

        /* Multiselect box text color */
        .stMultiSelect div[data-baseweb="select"] span {
            color: #2c3e50 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def data_visualization():
    set_custom_style()

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        st.page_link("Home.py", label="Home", icon="🌟")
        st.page_link("pages/Search.py", label="Property Search", icon="🔍")
        st.page_link("pages/Raw_Data_Visualization.py", label="Raw Data Visualization", icon="📊")

        st.markdown("---")
        with st.expander("Contact"):
            st.markdown("📧 support@example.com")
            st.markdown("📱 +82 10-1234-5678")

    # Main content
    st.title("Data Visualization")

    # Initialize session states
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'selected_columns' not in st.session_state:
        st.session_state.selected_columns = None
    if 'preprocessing_done' not in st.session_state:
        st.session_state.preprocessing_done = False
    if 'preprocessing_complete' not in st.session_state:
        st.session_state.preprocessing_complete = False
    if 'chart_type' not in st.session_state:
        st.session_state.chart_type = None
    if 'standardization' not in st.session_state:
        st.session_state.standardization = False
    if 'missing_values' not in st.session_state:
        st.session_state.missing_values = False
    if 'outliers' not in st.session_state:
        st.session_state.outliers = False
    if 'normalization' not in st.session_state:
        st.session_state.normalization = False

    # STEP 1: Data Selection
    with st.expander("STEP 1. Data Selection", expanded=st.session_state.current_step == 1):
        if 'file_uploader' not in st.session_state:
            st.session_state.file_uploader = None

        uploaded_file = st.file_uploader("Upload your data",
                                         type=["csv", "xlsx"],
                                         help="* File size must be less than 5MB",
                                         key="file_uploader")

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.df = pd.read_csv(uploaded_file)
                else:
                    st.session_state.df = pd.read_excel(uploaded_file)

                st.success("Data loaded successfully!")
                if st.button("Proceed to Preprocessing →", type="primary"):
                    st.session_state.current_step = 2
                    st.rerun()

            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
        else:
            st.session_state.df = None
            st.session_state.current_step = 1

    # STEP 2: Data Overview & Preprocessing
    if st.session_state.current_step >= 2:
        with st.expander("STEP 2. Data Overview & Preprocessing",
                         expanded=st.session_state.current_step == 2):
            if st.session_state.df is not None:
                # Sample data display
                st.subheader("Data Preview")
                st.dataframe(st.session_state.df.head(), hide_index=False)

                col1, col2 = st.columns([2, 1])
                with col1:
                    # Column selection
                    st.subheader("Select Columns")
                    selected_cols = st.multiselect(
                        "Choose columns for analysis:",
                        st.session_state.df.columns.tolist(),
                        default=st.session_state.selected_columns if st.session_state.selected_columns else None
                    )
                    # Update session state after selection
                    st.session_state.selected_columns = selected_cols

                with col2:
                    # Preprocessing methods with state preservation
                    st.subheader("Preprocessing Methods")
                    st.session_state.standardization = st.checkbox(
                        "Standardization",
                        value=st.session_state.standardization
                    )
                    st.session_state.missing_values = st.checkbox(
                        "Handle Missing Values",
                        value=st.session_state.missing_values
                    )
                    st.session_state.outliers = st.checkbox(
                        "Remove Outliers",
                        value=st.session_state.outliers
                    )
                    st.session_state.normalization = st.checkbox(
                        "Normalization",
                        value=st.session_state.normalization
                    )

                # Preprocessing buttons with state management
                if not st.session_state.preprocessing_complete:
                    if st.button("Apply Preprocessing", type="primary"):
                        # Perform preprocessing based on selected methods
                        if st.session_state.standardization:
                            # Add standardization logic here
                            pass
                        if st.session_state.missing_values:
                            # Add missing values handling logic here
                            pass
                        if st.session_state.outliers:
                            # Add outliers removal logic here
                            pass
                        if st.session_state.normalization:
                            # Add normalization logic here
                            pass

                        st.session_state.preprocessing_complete = True
                        st.success("Preprocessing completed successfully!")
                        st.rerun()

                if st.session_state.preprocessing_complete:
                    if st.button("Proceed to Visualization →", type="primary"):
                        st.session_state.current_step = 3
                        st.rerun()

    # STEP 3: Visualization
    if st.session_state.current_step >= 3:
        with st.expander("STEP 3. Visualization",
                         expanded=st.session_state.current_step == 3):
            # Chart type selection
            st.subheader("Select Chart Type")
            chart_col1, chart_col2, chart_col3, chart_col4 = st.columns(4)

            with chart_col1:
                if st.button("Bar", use_container_width=True):
                    st.session_state.chart_type = "bar"
            with chart_col2:
                if st.button("Scatter", use_container_width=True):
                    st.session_state.chart_type = "scatter"
            with chart_col3:
                if st.button("Pie", use_container_width=True):
                    st.session_state.chart_type = "pie"
            with chart_col4:
                if st.button("Donut", use_container_width=True):
                    st.session_state.chart_type = "donut"

            # Axis selection
            axis_col1, axis_col2 = st.columns(2)
            with axis_col1:
                x_axis = st.selectbox("X-Axis",
                                      options=[
                                                  ""] + st.session_state.selected_columns if st.session_state.selected_columns else [
                                          ""])
            with axis_col2:
                y_axis = st.selectbox("Y-Axis",
                                      options=[
                                                  ""] + st.session_state.selected_columns if st.session_state.selected_columns else [
                                          ""])

            # Generate visualization
            if st.button("Generate Visualization", type="primary"):
                if x_axis and y_axis:
                    chart_container = st.container()
                    with chart_container:
                        if st.session_state.chart_type == "bar":
                            fig = px.bar(st.session_state.df, x=x_axis, y=y_axis,
                                         title="Bar Chart")
                        elif st.session_state.chart_type == "scatter":
                            fig = px.scatter(st.session_state.df, x=x_axis, y=y_axis,
                                             title="Scatter Plot")
                        elif st.session_state.chart_type == "pie":
                            fig = px.pie(st.session_state.df, values=y_axis, names=x_axis,
                                         title="Pie Chart")
                        elif st.session_state.chart_type == "donut":
                            fig = px.pie(st.session_state.df, values=y_axis, names=x_axis,
                                         title="Donut Chart", hole=0.4)
                        else:
                            fig = px.bar(st.session_state.df, x=x_axis, y=y_axis,
                                         title="Visualization Result")

                        fig.update_layout(
                            plot_bgcolor="white",
                            paper_bgcolor="white",
                            font_color="#445566"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Please select both X and Y axes.")

    # Reset button at the bottom
    if st.session_state.current_step > 1:
        if st.button("Reset All"):
            # Reset all session states
            st.session_state.current_step = 1
            st.session_state.df = None
            st.session_state.selected_columns = None
            st.session_state.preprocessing_done = False
            st.session_state.preprocessing_complete = False
            st.session_state.chart_type = None
            st.session_state.standardization = False
            st.session_state.missing_values = False
            st.session_state.outliers = False
            st.session_state.normalization = False

            # Clear file uploader
            if 'file_uploader' in st.session_state:
                st.session_state.file_uploader = None

            # Rerun to refresh the page
            st.rerun()


if __name__ == "__main__":
    data_visualization()