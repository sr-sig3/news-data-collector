import pytest
from src.collector.news_collector import NewsCollector

@pytest.fixture
def collector():
    return NewsCollector()

def test_search_news(collector):
    # 테스트를 위한 검색어
    query = "코로나"
    news_list = collector.search_news(query, display=5)
    
    assert len(news_list) <= 5
    for news in news_list:
        assert news.title
        assert news.link
        assert news.description
        assert news.pub_date
        assert news.source

def test_get_latest_news(collector):
    query = "코로나"
    count = 3
    news_list = collector.get_latest_news(query, count)
    
    assert len(news_list) <= count
    for news in news_list:
        assert news.title
        assert news.link
        assert news.description
        assert news.pub_date
        assert news.source 
