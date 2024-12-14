import pandas as pd
import numpy as np
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv
import os
from gathering_data.data_gatherer import NaverRECrawler

load_dotenv()


def format_analysis_results(df, query_result):
    """
    데이터를 포맷팅하여 결과를 반환.
    """
    try:
        stats = {
            'Total Properties': len(df),
            'Unique Buildings': df['Name'].nunique(),
            'Average Price': df['MinPrice'].mean(),
            'Average Area': df['Area'].mean(),
            'Price Range': (df['MinPrice'].min(), df['MaxPrice'].max())
        }

        # 통계 및 결과 텍스트 포맷팅
        formatted_result = {
            "stats": stats,
            "top_properties": df.nlargest(5, 'MaxPrice')[['Name', 'MinPrice', 'MaxPrice', 'Area']],
            "affordable_properties": df.nsmallest(5, 'MinPrice')[['Name', 'MinPrice', 'MaxPrice', 'Area']],
            "query_result": query_result,
        }

        return formatted_result

    except Exception as e:
        return {"error": f"Formatting error: {str(e)}"}


from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd


def format_analysis_results(df, query_result):
    """
    Format the analysis results into a structured output.
    """
    try:
        stats = {
            'Total Properties': len(df),
            'Unique Buildings': df['Name'].nunique(),
            'Average Price': df['MinPrice'].mean(),
            'Average Area': df['Area'].mean(),
            'Price Range': (df['MinPrice'].min(), df['MaxPrice'].max())
        }

        formatted_result = {
            "stats": stats,
            "top_properties": df.nlargest(5, 'MaxPrice')[['Name', 'MinPrice', 'MaxPrice', 'Area']],
            "affordable_properties": df.nsmallest(5, 'MinPrice')[['Name', 'MinPrice', 'MaxPrice', 'Area']],
            "query_result": query_result
        }
        return formatted_result
    except Exception as e:
        return {"error": f"Formatting error: {str(e)}"}


def run(input_query, model, location=None, data=None):
    try:
        # Data retrieval
        if data is None and location is not None:
            crawler = NaverRECrawler()
            data = crawler.search_location(location)
        elif data is None:
            raise ValueError("Either location or data must be provided")

        # Column mapping
        column_mapping = {
            'Name': 'Name',
            'minDeal': 'MinPrice',
            'maxDeal': 'MaxPrice',
            'representativeArea': 'Area',
            'Type': 'PropertyType'
        }

        df = data[list(column_mapping.keys())].copy()
        df.columns = list(column_mapping.values())

        # OpenAI model handling
        if model == "openai":
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found")

            llm = OpenAI(api_token=OPENAI_API_KEY, model_name="gpt-4")
            sdf = SmartDataframe(df, config={
                "llm": llm,
                "verbose": True,
                "enable_cache": True
            })

            prompt = f"""
            Analyze the real estate data for the following query: {input_query}

            Return a dictionary with the following structure:
            {{
                "type": "string",
                "value": "<your analysis here>"
            }}

            Include in your analysis:
            1. A brief summary of findings
            2. Specific insights related to the query
            3. Notable properties that match the criteria
            """

            result = sdf.chat(prompt)

            # Ensure proper output format
            if isinstance(result, dict) and "type" in result and "value" in result:
                return df, result
            else:
                # Format the result if it's not already in the correct format
                formatted_result = {
                    "type": "string",
                    "value": str(result)
                }
                return df, formatted_result

        return df, {"type": "string", "value": "Model not supported."}

    except Exception as e:
        return None, {"type": "error", "value": f"Error occurred: {str(e)}"}


if __name__ == "__main__":
    try:
        crawler = NaverRECrawler()
        location = input("Enter location to search (e.g., Gangnam Station): ")
        df = crawler.search_location(location)
        print(f"\nSuccessfully loaded data for {location}")

        while True:
            test_input = input("\nEnter your query (or 'q' to quit): ")
            if test_input.lower() == 'q':
                break
            print("\nAnalyzing your query...")
            result = run(test_input, "openai", data=df)
            print(result)
    except Exception as e:
        print(f"Program error: {str(e)}")