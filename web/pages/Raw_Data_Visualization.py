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
        h1 { color: #2c3e50; font-weight: 600; }
        h2 { color: #34495e; font-weight: 500; }
        h3 { color: #445566; font-weight: 500; }

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
            transition: background-color 0.3s ease;
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

        /* DataFrames */
        .dataframe {
            background-color: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }

        /* Checkbox container */
        .checkbox-container {
            max-height: 300px;
            overflow-y: auto;
            padding-right: 10px;
            background-color: white;
            border-radius: 6px;
            border: 1px solid #e1e4e8;
        }

        /* Checkbox styling */
        .stCheckbox {
            margin-bottom: 0.5rem;
        }

        /* Scrollbar styling */
        .checkbox-container::-webkit-scrollbar {
            width: 6px;
        }

        .checkbox-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 3px;
        }

        .checkbox-container::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 3px;
        }

        .checkbox-container::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'selected_columns' not in st.session_state:
        st.session_state.selected_columns = []
    if 'preprocessing_complete' not in st.session_state:
        st.session_state.preprocessing_complete = False
    if 'chart_type' not in st.session_state:
        st.session_state.chart_type = None
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = 0
    if 'x_axis' not in st.session_state:
        st.session_state.x_axis = None
    if 'y_axis' not in st.session_state:
        st.session_state.y_axis = None


def reset_session_state():
    if 'file_uploader_key' in st.session_state:
        st.session_state.file_uploader_key += 1
    for key in list(st.session_state.keys()):
        if key != 'file_uploader_key':
            del st.session_state[key]
    initialize_session_state()


def handle_preprocessing():
    """전처리 로직을 처리하는 함수"""
    return True


def data_visualization():
    set_custom_style()

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/Search.py", label="Search", icon="🔍")
        st.page_link("pages/Raw_Data_Visualization.py", label="Raw Data Visualization", icon="📊")

        st.markdown("---")
        with st.expander("Contact"):
            st.markdown("📧 support@example.com")
            st.markdown("📱 +82 10-1234-5678")

    st.title("Data Visualization")
    initialize_session_state()

    # STEP 1: Data Selection
    with st.expander("STEP 1. Data Selection", expanded=st.session_state.current_step == 1):
        uploaded_file = st.file_uploader(
            "Upload your data",
            type=["csv", "xlsx"],
            help="* File size must be less than 200MB",
            key=f"file_uploader_{st.session_state.file_uploader_key}"
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.df = pd.read_csv(uploaded_file)
                else:
                    st.session_state.df = pd.read_excel(uploaded_file)

                if st.button("Proceed to Preprocessing →", type="primary"):
                    st.session_state.current_step = 2
                    st.rerun()

            except Exception as e:
                st.error(f"Error loading data: {str(e)}")

    # STEP 2: Data Overview & Preprocessing
    if st.session_state.current_step >= 2:
        with st.expander("STEP 2. Data Overview & Preprocessing", expanded=st.session_state.current_step == 2):
            if st.session_state.df is not None:
                st.subheader("Data Preview")
                st.dataframe(st.session_state.df.head(), hide_index=False)

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("Select Columns")
                    columns = st.session_state.df.columns.tolist()

                    # Select All 체크박스 추가
                    select_all = st.checkbox("Select All",
                                             value=len(st.session_state.selected_columns) == len(columns),
                                             key="select_all")

                    st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)

                    # 컬럼별 체크박스
                    selected = {}
                    for col in columns:
                        if select_all:
                            selected[col] = True
                            if col not in st.session_state.selected_columns:
                                st.session_state.selected_columns.append(col)
                        else:
                            selected[col] = st.checkbox(
                                col,
                                value=col in st.session_state.selected_columns,
                                key=f"col_{col}"
                            )

                            if selected[col] and col not in st.session_state.selected_columns:
                                st.session_state.selected_columns.append(col)
                            elif not selected[col] and col in st.session_state.selected_columns:
                                st.session_state.selected_columns.remove(col)

                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.subheader("Preprocessing Methods")
                    standardization = st.checkbox("Standardization")
                    missing_values = st.checkbox("Handle Missing Values")
                    outliers = st.checkbox("Remove Outliers")
                    normalization = st.checkbox("Normalization")

                preprocessing_col = st.container()
                with preprocessing_col:
                    if not st.session_state.preprocessing_complete:
                        if st.button("Apply Preprocessing", type="primary"):
                            if handle_preprocessing():
                                st.session_state.preprocessing_complete = True
                                st.rerun()

                    if st.session_state.preprocessing_complete:
                        if st.button("Proceed to Visualization →", type="primary"):
                            st.session_state.current_step = 3
                            st.rerun()

    # STEP 3: Visualization
    if st.session_state.current_step >= 3:
        with st.expander("STEP 3. Visualization", expanded=st.session_state.current_step == 3):
            st.subheader("Select Chart Type")

            chart_types = ["bar", "scatter", "pie", "donut"]
            cols = st.columns(4)

            for i, chart_type in enumerate(chart_types):
                with cols[i]:
                    button_style = "primary" if st.session_state.chart_type == chart_type else "secondary"
                    if st.button(chart_type.title(), use_container_width=True, type=button_style):
                        st.session_state.chart_type = chart_type
                        st.rerun()

            if st.session_state.selected_columns:
                axis_col1, axis_col2 = st.columns(2)
                with axis_col1:
                    x_axis = st.selectbox(
                        "X-Axis",
                        options=st.session_state.selected_columns,
                        index=0 if st.session_state.x_axis is None else st.session_state.selected_columns.index(
                            st.session_state.x_axis),
                        key="x_axis_select"
                    )
                    st.session_state.x_axis = x_axis

                with axis_col2:
                    y_axis = st.selectbox(
                        "Y-Axis",
                        options=st.session_state.selected_columns,
                        index=0 if st.session_state.y_axis is None else st.session_state.selected_columns.index(
                            st.session_state.y_axis),
                        key="y_axis_select"
                    )
                    st.session_state.y_axis = y_axis

                if st.button("Generate Visualization", type="primary"):
                    if x_axis and y_axis and st.session_state.chart_type:
                        fig = None
                        if st.session_state.chart_type == "bar":
                            fig = px.bar(st.session_state.df, x=x_axis, y=y_axis, title="Bar Chart")
                        elif st.session_state.chart_type == "scatter":
                            fig = px.scatter(st.session_state.df, x=x_axis, y=y_axis, title="Scatter Plot")
                        elif st.session_state.chart_type == "pie":
                            fig = px.pie(st.session_state.df, values=y_axis, names=x_axis, title="Pie Chart")
                        elif st.session_state.chart_type == "donut":
                            fig = px.pie(st.session_state.df, values=y_axis, names=x_axis, title="Donut Chart",
                                         hole=0.4)

                        if fig:
                            fig.update_layout(
                                plot_bgcolor="white",
                                paper_bgcolor="white",
                                font_color="#445566"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Please select both axes and a chart type.")

    # Reset button
    if st.session_state.current_step > 1:
        if st.button("Reset All"):
            reset_session_state()
            st.rerun()


if __name__ == "__main__":
    data_visualization()