# from gathering_data.classes import *
from gathering_data.util import *
import requests
import pandas as pd
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()


class NaverRECrawler:
    def __init__(self, coord_file="gathering_data/data/bjd_info_except_boundary.csv"):
        # 기본 좌표 (Fallback)
        self.default_coordinates = {
            "강남역": (37.4979462, 127.0276206),
            "역삼역": (37.5006, 127.0368),
            "선릉역": (37.5044, 127.0505),
            "서울역": (37.5551, 126.9707),
            "한강공원": (37.5662, 126.8763),
            "홍대입구역": (),
            "이태원역": (),
            "부산역": (),
            "대전역": (),
        }
        # 파일에서 좌표 로드
        self.coordinates = self.load_coordinates_from_file(coord_file)

    def load_coordinates_from_file(self, file_path):
        """Load coordinates from CSV file."""
        data = pd.read_csv(file_path, encoding="cp949")
        coordinates = {
            row["bjd_nm"]: (row["center_lati"], row["center_long"])
            for _, row in data.iterrows()
        }
        return coordinates

    def get_coordinates(self, query):
        """Get coordinates by query from loaded data or fallback."""
        if query in self.coordinates:
            return NLocation(*self.coordinates[query])
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
    try:
        coord_file = "gathering_data/data/bjd_info_except_boundary.csv"
        crawler = NaverRECrawler(coord_file)

        location = input("검색할 위치를 입력하세요 (예: 강남역): ")
        df = crawler.search_location(location)

        print(f"\n총 {len(df)}개의 매물이 검색되었습니다.")
        print(df.head())

        output_file = f"{location}_real_estate_data.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n데이터가 {output_file}로 저장되었습니다.")
    except Exception as e:
        print(f"Error: {str(e)}")