from src.collector.news_collector import NewsCollector
from datetime import datetime
from config.categories import CATEGORIES

def main():
    # 뉴스 수집기 인스턴스 생성
    collector = NewsCollector()
    
    # 검색할 분야 설정
    categories = ["경제", "IT", "스포츠"]
    
    # 각 분야별로 뉴스 수집
    for category in categories:
        print(f"\n=== {category} 분야 최신 뉴스 ===")
        
        try:
            # 최신 뉴스 5개 가져오기
            news_list = collector.get_category_news(category, count=5)
            
            # 뉴스 출력
            for i, news in enumerate(news_list, 1):
                print(f"\n{i}. {news.title}")
                print(f"   링크: {news.link}")
                print(f"   설명: {news.description}")
                print(f"   발행일: {news.pub_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   출처: {news.source}")
                
        except Exception as e:
            print(f"'{category}' 분야 검색 중 오류 발생: {str(e)}")

    for category in categories:
        collector.collect_and_send_news(category, count=5)

if __name__ == "__main__":
    main() 
    