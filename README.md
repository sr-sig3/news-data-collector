# News Data Collector

뉴스 데이터를 수집하고 처리하는 프로젝트입니다.

## 설치 방법

1. 저장소를 클론합니다:
```bash
git clone [repository-url]
cd news-data-collector
```

2. 가상환경을 생성하고 활성화합니다:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

4. `.env` 파일을 생성하고 네이버 API 키를 설정합니다:
```
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
```

## 사용 방법

```python
from src.collector.naver_news import NaverNewsCollector

collector = NaverNewsCollector()
news_list = collector.get_latest_news("검색어", count=10)

for news in news_list:
    print(f"제목: {news.title}")
    print(f"링크: {news.link}")
    print(f"설명: {news.description}")
    print(f"발행일: {news.pub_date}")
    print(f"출처: {news.source}")
    print("---")
```

## 테스트 실행

```bash
pytest tests/
```
