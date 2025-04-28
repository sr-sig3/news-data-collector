from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'topic': os.getenv('KAFKA_TOPIC', 'news-topic'),
    'client_id': os.getenv('KAFKA_CLIENT_ID', 'news-collector')
} 