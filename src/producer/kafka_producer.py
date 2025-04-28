from kafka import KafkaProducer
import json
from typing import Dict, Any
from config.kafka_config import KAFKA_CONFIG

class NewsKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_CONFIG['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            client_id=KAFKA_CONFIG['client_id']
        )
        self.topic = KAFKA_CONFIG['topic']

    def send_news(self, news_data: Dict[str, Any]) -> None:
        """
        뉴스 데이터를 Kafka로 전송합니다.
        
        Args:
            news_data (Dict[str, Any]): 전송할 뉴스 데이터
        """
        try:
            # 메시지 전송
            future = self.producer.send(
                topic=self.topic,
                value=news_data
            )
            
            # 전송 결과 확인 (선택사항)
            future.get(timeout=10)
            
        except Exception as e:
            print(f"Error sending message to Kafka: {str(e)}")
            raise

    def close(self) -> None:
        """Producer를 종료합니다."""
        self.producer.close() 