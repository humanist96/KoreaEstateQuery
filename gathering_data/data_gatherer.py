from crawl4ai import Crawler, Selector
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


class NaverLandCrawler(Crawler):
    def __init__(self, base_url="https://land.naver.com/"):
        super().__init__()
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    def parse_listings(self, html_content):
        # Use Selector from Crawl4AI to parse HTML
        selector = Selector(html_content)
        listings = []

        # Select elements containing property information
        for item in selector.css("div.c_aside"):
            try:
                name = item.css("span.title::text").get()
                price = item.css("span.price::text").get()
                area = item.css("span.area::text").get()
                address = item.css("span.address::text").get()
                link = item.css("a::attr(href)").get()

                listings.append({
                    "Name": name,
                    "Price": price,
                    "Area": area,
                    "Address": address,
                    "Link": f"{self.base_url}{link}" if link else None
                })
            except Exception as e:
                print(f"Error parsing item: {e}")

        return listings

    def crawl(self, query):
        search_url = f"{self.base_url}search/search.naver?query={query}"
        html_content = self.fetch_page(search_url)
        if not html_content:
            return []

        listings = self.parse_listings(html_content)
        return listings

    def save_to_excel(self, data, file_name="output.xlsx"):
        if not data:
            print("No data to save.")
            return

        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")


if __name__ == "__main__":
    crawler = NaverLandCrawler()
    location = input("검색할 지역을 입력하세요 (예: 강남역): ")

    try:
        listings = crawler.crawl(location)
        print(f"총 {len(listings)}개의 매물이 검색되었습니다.")

        # 미리 보기 출력
        for item in listings[:5]:
            print(item)

        # 엑셀로 저장
        output_file = f"{location}_real_estate_listings.xlsx"
        crawler.save_to_excel(listings, output_file)
    except Exception as e:
        print(f"Error during crawling: {e}")
