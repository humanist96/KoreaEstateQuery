# search.py
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sys
from pathlib import Path



# Set project root directory
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from analysis.PandasAI_Analysis import run, format_analysis_results

load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="Korea Real Estate Search", layout="centered")

# Available locations and predefined queries
LOCATIONS = ["강남역", "서울역", "한강공원", "홍대입구역", "이태원역", "부산역", "대전역"]
LOCATION_MAPPING = {
    "강남역": "Gangnam Station",
    "서울역": "Seoul Station",
    "한강공원": "Hangang Park",
    "홍대입구역": "Hongdae Station",
    "이태원역": "Itaewon Station",
    "부산역": "Busan Station",
    "대전역": "Daejeon Station"
}

PREDEFINED_QUERIES = {
    "가격 관련": [
        "3억원 이하의 매물 찾기",
        "월세가 가장 낮은 top 3 매물은?",
        "평당 가격이 가장 낮은 매물은?"
    ],
    "면적/구조 관련": [
        "남향이면서 넓은 면적의 매물 추천",
        "20평 이상의 매물 목록",
        "주차 공간이 있는 매물만 보여주기"
    ],
    "건물 상태": [
        "2010년 이후 지어진 건물 보여주기",
        "리모델링된 매물 찾기",
        "관리상태가 좋은 매물 추천"
    ]
}


def initialize_session_state():
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None


def main():
    initialize_session_state()

    st.title("🏢 Korea Real Estate Search")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Location selector
        selected_location = st.selectbox(
            "Select Location",
            LOCATIONS
        )
        selected_location_eng = LOCATION_MAPPING[selected_location]

        # Query input method selection
        query_method = st.radio(
            "Choose Search Method",
            ["Direct Input", "Predefined Questions"]
        )

        search_query = ""

        if "Direct" in query_method:
            search_query = st.text_input(
                "Enter your question",
                placeholder="예시: 남향이면서 넓은 면적의 매물 추천"
            )
        else:
            # Category selection
            category = st.selectbox(
                "Select Category",
                list(PREDEFINED_QUERIES.keys())
            )

            # Query selection from category
            if category:
                search_query = st.selectbox(
                    "Select Question",
                    PREDEFINED_QUERIES[category]
                )

    with col2:
        st.subheader("Search History")
        if st.session_state.search_history:
            for idx, (loc, query, time) in enumerate(st.session_state.search_history[-5:]):
                st.text(f"{time}\n{loc}: {query}")
        else:
            st.text("No search history available")

    if st.button("Search"):
        if search_query:
            with st.spinner(f"Analyzing data for {selected_location}..."):
                try:
                    # Run the analysis
                    contextualized_query = f"{selected_location} ({selected_location_eng}): {search_query}"
                    df, query_result = run(contextualized_query, "openai", location=selected_location)

                    # 분석 결과 포맷팅
                    if df is not None:
                        # 1. 중복 제거 ('Name' 기준, 첫 번째 값 유지)
                        df_cleaned = df.drop_duplicates(subset='Name', keep='first')

                        # 2. 특정 칼럼 값이 0인 행 제거 (예: 'Price'가 0인 데이터 제거)
                        df_cleaned = df_cleaned[df_cleaned['MaxPrice'] != 0]

                        formatted_result = format_analysis_results(df_cleaned, query_result)

                        # 결과 표시
                        st.success("Search completed.")
                        st.markdown("### **📊 Analysis Summary**")

                        # 통계 정보 표시
                        stats = formatted_result["stats"]
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Properties", f"{stats['Total Properties']:,}")
                            # st.metric("평균 가격", f"{stats['Average Price']:.2f}억 원")
                        with col2:
                            st.metric("Unique Buildings", f"{stats['Unique Buildings']:,}")
                            # st.metric("최저가", f"{stats['Price Range'][0]:.2f}억 원")
                        with col3:
                            st.metric("Average Area", f"{stats['Average Area']:.1f}㎡")
                            # st.metric("최고가", f"{stats['Price Range'][1]:.2f}억 원")

                        # OpenAI 분석 결과
                        st.markdown("### **Analysis Results**")
                        st.dataframe(formatted_result["query_result"][:20])

                        # 최고가 매물
                        st.markdown("### **Top 5 Highest Priced Properties**")
                        st.table(formatted_result["top_properties"])

                        # 저가 매물
                        st.markdown("### **Top 5 Affordable Properties**")
                        st.table(formatted_result["affordable_properties"])

                    else:
                        st.error("Failed to load data")

                except Exception as e:
                    st.error(f"An error occurred during search: {str(e)}")

    # Footer with instructions
    st.markdown("---")
    st.markdown("""
    **Search Tips:**
    - Enter specific details about what you're looking for
    - You can mention price range, preferred area, building condition, etc.
    - Use predefined questions for common queries
    """)

if __name__ == "__main__":
    main()