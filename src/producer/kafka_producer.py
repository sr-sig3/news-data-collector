from kafka import KafkaProducer
import json
from typing import Dict, Any
import structlog
from config.kafka_config import KAFKA_CONFIG

logger = structlog.get_logger()

class NewsKafkaProducer:
    def __init__(self):
        logger.info("initializing_kafka_producer",
                   bootstrap_servers=KAFKA_CONFIG['bootstrap_servers'],
                   topic=KAFKA_CONFIG['topic'])
        
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[KAFKA_CONFIG['bootstrap_servers']],  # 리스트로 감싸서 전달
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                client_id=KAFKA_CONFIG['client_id'],
                acks='all',  # 모든 복제본이 메시지를 받았는지 확인
                retries=3,   # 실패 시 3번 재시도
                retry_backoff_ms=1000,  # 재시도 간격 1초
                request_timeout_ms=30000  # 요청 타임아웃 30초
            )
            self.topic = KAFKA_CONFIG['topic']
            logger.info("kafka_producer_initialized_successfully")
            
        except Exception as e:
            logger.error("kafka_producer_initialization_failed",
                        error=str(e),
                        error_type=type(e).__name__)
            raise

    def send_news(self, news_data: Dict[str, Any]) -> None:
        """뉴스 데이터를 Kafka로 전송합니다."""
        try:
            logger.info("sending_news",
                       title=news_data.get('title', 'unknown'),
                       topic=self.topic)
            
            # 메시지 전송
            future = self.producer.send(
                topic=self.topic,
                value=news_data
            )
            
            # 전송 결과 확인
            result = future.get(timeout=30)  # 타임아웃 30초로 증가
            logger.info("message_sent_successfully",
                       topic=result.topic,
                       partition=result.partition,
                       offset=result.offset)
            
        except Exception as e:
            logger.error("error_sending_message",
                        error=str(e),
                        error_type=type(e).__name__)
            raise

    def close(self) -> None:
        """Producer를 종료합니다."""
        try:
            logger.info("closing_kafka_producer")
            self.producer.close(timeout=5)
            logger.info("kafka_producer_closed_successfully")
        except Exception as e:
            logger.error("error_closing_kafka_producer",
                        error=str(e),
                        error_type=type(e).__name__) 