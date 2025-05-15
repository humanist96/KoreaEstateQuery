from gathering_data.classes import *
from gathering_data.util import *
import requests
import pandas as pd
import urllib.parse
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]

class NaverRECrawler:
    def __init__(self):
        self.default_coordinates = {
            "강남역": (37.4979462, 127.0276206),
            "역삼역": (37.5006, 127.0368),
            "선릉역": (37.5044, 127.0505),
        }
        self.api_key = st.secrets["google_api_key"]

    def get_coordinates(self, query):
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_query}&key={self.api_key}"

        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK" and data["results"]:
                    location = data["results"][0]["geometry"]["location"]
                    return NLocation(float(location["lat"]), float(location["lng"]))
        except Exception as e:
            print(f"API Error: {str(e)}")

        if query in self.default_coordinates:
            return NLocation(*self.default_coordinates[query])

        raise Exception(f"Location not found for: {query}")

    def search_location(self, query):
        location = self.get_coordinates(query)
        print(f"Searching around coordinates: {location}")
        sector = get_sector(location)
        return self._get_real_estate_data(sector)

    def _get_real_estate_data(self, sector):
        things = get_things_each_direction(sector)
        neighbors = get_all_neighbors(sector)
        update_things_intersection(things, neighbors, get_distance_standard())
        df = pd.DataFrame([t.get_list() for t in things], columns=NThing.HEADER)

        # 가격 단위 변환 (만원 -> 억원)
        price_columns = [
            "minDeal",
            "maxDeal",
            "medianDeal",
            "minLease",
            "maxLease",
            "medianLease",
        ]
        for col in price_columns:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: round(x / 10000, 2) if pd.notnull(x) else x
                )

        return df


if __name__ == "__main__":
    crawler = NaverRECrawler()
    try:
        location = input("검색할 위치를 입력하세요 (예: 강남역): ")
        df = crawler.search_location(location)

        print(f"\n총 {len(df)}개의 매물이 검색되었습니다.")
        columns_to_show = [
            "Name",
            "Type",
            "Build",
            "minDeal",
            "maxDeal",
            "representativeArea",
        ]
        print(df[columns_to_show].head())

        output_file = f"{location}_real_estate_data.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n데이터가 {output_file}로 저장되었습니다.")
    except Exception as e:
        print(f"Error: {str(e)}")
