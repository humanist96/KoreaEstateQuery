from openai import OpenAI
import pandas as pd
from analysis.prompts import RealEstatePrompts


class RealEstateAnalyzer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze_properties(self, df: pd.DataFrame, query: str) -> str:
        """Analyze property data using OpenAI"""
        try:
            if df.empty:
                return RealEstatePrompts.get_error_message()

            # Convert DataFrame to a formatted string
            data_str = df.to_string()

            # Get analysis prompt
            prompt = RealEstatePrompts.get_analysis_prompt(query)

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a Korean real estate market expert."},
                    {"role": "user", "content": f"Here is the property data:\n{data_str}\n\n{prompt}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return RealEstatePrompts.get_error_message()