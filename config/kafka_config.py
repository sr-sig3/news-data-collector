from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'topic': os.getenv('KAFKA_TOPIC'),
    'client_id': os.getenv('KAFKA_CLIENT_ID')
} 