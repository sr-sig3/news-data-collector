import requests
from typing import List, Dict, Optional, Set, Any
from ..models.news import News
from config.config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, NAVER_NEWS_SEARCH_URL, DEFAULT_SEARCH_PARAMS
from config.categories import CATEGORIES
from datetime import datetime
from ..producer.kafka_producer import NewsKafkaProducer
import logging
import time
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        logger.info("Initializing NewsCollector")
        self.headers = {
            'X-Naver-Client-Id': NAVER_CLIENT_ID,
            'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
        }
        self.kafka_producer = NewsKafkaProducer()
        self.request_delay = 0.1  # 100ms 딜레이

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def search_news(self, query: str, display: int = 10, start: int = 1, 
                   sort: str = 'date', media: Optional[str] = None) -> List[News]:
        """
        뉴스 검색 API를 사용하여 뉴스를 검색합니다.
        
        Args:
            query (str): 검색어
            display (int): 한 번에 표시할 검색 결과 개수
            start (int): 검색 시작 위치
            sort (str): 정렬 기준 ('date': 날짜순, 'sim': 관련도순)
            media (str, optional): 특정 언론사 이름
            
        Returns:
            List[News]: 검색된 뉴스 목록
        """
        params = DEFAULT_SEARCH_PARAMS.copy()
        params.update({
            'query': query,
            'display': display,
            'start': start,
            'sort': sort
        })

        try:
            # API 요청 전 딜레이
            time.sleep(self.request_delay)
            
            response = requests.get(
                NAVER_NEWS_SEARCH_URL,
                headers=self.headers,
                params=params
            )
            
            # 429 에러 (Too Many Requests) 발생 시 딜레이 증가
            if response.status_code == 429:
                logger.warning("Rate limit exceeded, increasing delay")
                self.request_delay *= 2
                time.sleep(1)  # 1초 대기
                return self.search_news(query, display, start, sort, media)
            
            response.raise_for_status()

            data = response.json()
            news_list = [News.create_from_response(item) for item in data['items']]
            
            # 특정 언론사 필터링
            if media:
                news_list = [news for news in news_list if media in news.source]
            
            return news_list
            
        except RequestException as e:
            logger.error(f"Error searching news: {str(e)}")
            if "429" in str(e):
                logger.warning("Rate limit exceeded, waiting before retry")
                time.sleep(1)
                return self.search_news(query, display, start, sort, media)
            raise

    def get_latest_news(self, query: str, count: int = 10, 
                       media: Optional[str] = None) -> List[News]:
        """
        최신 뉴스를 검색합니다.
        
        Args:
            query (str): 검색어
            count (int): 검색할 뉴스 개수
            media (str, optional): 특정 언론사 이름
            
        Returns:
            List[News]: 검색된 뉴스 목록
        """
        all_news = []
        start = 1
        
        while len(all_news) < count:
            try:
                news = self.search_news(
                    query, 
                    display=min(100, count - len(all_news)), 
                    start=start,
                    media=media
                )
                if not news:
                    break
                all_news.extend(news)
                start += len(news)
                
            except Exception as e:
                logger.error(f"Error getting latest news: {str(e)}")
                break
            
        return all_news[:count]

    def get_category_news(self, category: str, count: int = 10) -> List[News]:
        """
        특정 분야의 최신 뉴스를 검색합니다.
        
        Args:
            category (str): 뉴스 분야 (예: "경제", "정치", "IT" 등)
            count (int): 검색할 뉴스 개수
            
        Returns:
            List[News]: 검색된 뉴스 목록
        """
        if category not in CATEGORIES:
            raise ValueError(f"지원하지 않는 분야입니다: {category}")
        
        category_config = CATEGORIES[category]
        all_news = []
        seen_links = set()  # 중복 뉴스 제거를 위한 링크 저장
        
        # 각 키워드별로 뉴스 검색
        for keyword in category_config["keywords"]:
            if len(all_news) >= count:
                break
                
            # 각 언론사별로 뉴스 검색
            for media in category_config["media"]:
                if len(all_news) >= count:
                    break
                    
                try:
                    news_list = self.get_latest_news(
                        keyword,
                        count=min(5, count - len(all_news)),
                        media=media
                    )
                    
                    # 중복되지 않은 뉴스만 추가
                    for news in news_list:
                        if news.link not in seen_links:
                            all_news.append(news)
                            seen_links.add(news.link)
                            
                except Exception as e:
                    logger.error(f"Error getting news for {category} - {keyword} - {media}: {str(e)}")
                    continue
                        
        return all_news[:count]

    def collect_and_send_news(self, query: str, count: int = 10) -> None:
        """
        뉴스를 수집하고 Kafka로 전송합니다.
        
        Args:
            query (str): 검색어
            count (int): 수집할 뉴스 개수
        """
        try:
            logger.info(f"Collecting news for query: {query}, count: {count}")
            # 뉴스 수집
            news_list = self.search_news(query, count)
            logger.info(f"Collected {len(news_list)} news items")
            
            # 각 뉴스를 Kafka로 전송
            for news in news_list:
                news_data = {
                    'title': news.title,
                    'link': news.link,
                    'description': news.description,
                    'pub_date': news.pub_date.isoformat(),
                    'source': news.source,
                    'collected_at': datetime.now().isoformat()
                }
                logger.info(f"Preparing to send news: {news.title}")
                self.kafka_producer.send_news(news_data)
                
        except Exception as e:
            logger.error(f"Error in collect_and_send_news: {str(e)}")
            raise

    def close(self):
        """Kafka Producer를 명시적으로 닫습니다."""
        logger.info("Closing NewsCollector")
        self.kafka_producer.close() 
