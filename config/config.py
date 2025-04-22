import os
from dotenv import load_dotenv

load_dotenv()

# Naver API Credentials
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

# API Endpoints
NAVER_NEWS_SEARCH_URL = "https://openapi.naver.com/v1/search/news.json"

# Search Parameters
DEFAULT_SEARCH_PARAMS = {
    'query': '',
    'display': 10,  # 한 번에 표시할 검색 결과 개수
    'start': 1,     # 검색 시작 위치
    'sort': 'date'  # 정렬 기준 (date: 날짜순)
} 
