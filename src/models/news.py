from dataclasses import dataclass
from datetime import datetime

@dataclass
class News:
    title: str
    link: str
    description: str
    pub_date: datetime
    source: str

    @classmethod
    def create_from_response(cls, item: dict) -> 'News':
        """네이버 API 응답으로부터 News 객체를 생성합니다."""
        return cls(
            title=item['title'],
            link=item['link'],
            description=item['description'],
            pub_date=datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z'),
            source=item.get('originallink', '')  # source 대신 originallink 사용
        ) 
        