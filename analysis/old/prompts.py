class RealEstatePrompts:
    @staticmethod
    def get_analysis_prompt(query: str) -> str:
        return f"""
        As a Korean real estate market expert, analyze the following query: {query}

        Please provide a comprehensive analysis including:
        1. Key Market Insights:
           - Overall market assessment for the specified area
           - Price trends and patterns
           - Notable property characteristics

        2. Specific Recommendations:
           - Best matching properties based on the query
           - Investment potential
           - Area-specific advantages and considerations

        3. Local Context:
           - Neighborhood characteristics
           - Proximity to facilities and transportation
           - Future development plans (if applicable)

        Guidelines:
        - Focus on providing actionable insights
        - Consider Korean market specifics and local context
        - Include both quantitative and qualitative analysis
        - Highlight any unique opportunities or concerns
        - Use appropriate Korean real estate terminology where relevant

        Format the response in clear, organized sections with headers.
        """

    @staticmethod
    def get_error_message() -> str:
        return """
        I apologize, but I couldn't retrieve or analyze the property data at this moment. 
        This might be due to:
        - Temporary access issues with the real estate database
        - Network connectivity problems
        - Invalid location input

        Please try again with:
        - A more specific location name
        - Korean characters for better accuracy
        - Checking your internet connection
        """