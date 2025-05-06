from kafka import KafkaProducer
import json
from typing import Dict, Any
from config.kafka_config import KAFKA_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsKafkaProducer:
    def __init__(self):
        logger.info(f"Initializing Kafka producer with config: {KAFKA_CONFIG}")
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_CONFIG['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            client_id=KAFKA_CONFIG['client_id']
        )
        self.topic = KAFKA_CONFIG['topic']
        logger.info(f"Kafka producer initialized for topic: {self.topic}")

    def send_news(self, news_data: Dict[str, Any]) -> None:
        """
        뉴스 데이터를 Kafka로 전송합니다.
        
        Args:
            news_data (Dict[str, Any]): 전송할 뉴스 데이터
        """
        try:
            logger.info(f"Sending news to topic {self.topic}: {news_data['title']}")
            # 메시지 전송
            future = self.producer.send(
                topic=self.topic,
                value=news_data
            )
            
            # 전송 결과 확인
            result = future.get(timeout=10)
            logger.info(f"Message sent successfully: {result}")
            
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {str(e)}")
            raise

    def close(self) -> None:
        """Producer를 종료합니다."""
        logger.info("Closing Kafka producer")
        self.producer.close() 