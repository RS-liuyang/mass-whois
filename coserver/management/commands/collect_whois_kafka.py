from django.core.management.base import BaseCommand
from time import sleep

from random import randint
from mass_whois.config import get_config
from pykafka import KafkaClient
from coserver.models import whoisRaw
import json

class Command(BaseCommand):
    help = 'Collect WHOIS results from Kafka'

    def handle(self, *args, **options):
        kafka_host = None

        while not kafka_host:
            kafka_host = get_config('KAFKA_HOST')

            if not kafka_host:
                print 'Unable to get Kafka host address, will try again.'
                sleep(randint(2, 5))

        client = KafkaClient(hosts=kafka_host)
        topic = client.topics['results']

        consumer = topic.get_simple_consumer()

        for message in consumer:
            if message is None:
                continue

            msg = json.loads(message.value)

            whoisRaw.objects.create(name=msg['qname'], update_time=msg['Timestamp'], result_json=msg['result'])
