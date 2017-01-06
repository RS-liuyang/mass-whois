from django.conf import settings
from pykafka import KafkaClient
from mass_whois.config import get_config
import pythonwhois
import json
from datetime import datetime


def send_to_kafka(topic_name, msg):
    kafka_host = get_config('KAFKA_HOST')

    if not kafka_host:
        raise Exception('Unable to get Kafka host address')

    client = KafkaClient(hosts=kafka_host)
    topic = client.topics[topic_name]

    with topic.get_producer(delivery_reports=True) as producer:
        producer.produce(json.dumps(msg, sort_keys=True))

        msg, exc = producer.get_delivery_report(block=True)

        if exc is not None:
            raise exc


def json_fallback(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


def whois(name):
    result = '-1'

    try:
        data, server_list = pythonwhois.net.get_whois_raw(name, with_server_list=True)
        if len(server_list) > 0:
            parsed = pythonwhois.parse.parse_raw_whois(data, normalized=True, never_query_handles=False,
                                                       handle_server=server_list[-1])
        else:
            parsed = pythonwhois.parse.parse_raw_whois(data, normalized=True)

        result = json.dumps(parsed, default=json_fallback)
    except Exception, e:
        result = e.message

    kafka_msg = {'qname': name,
                 'result': result,
                 'Timestamp': datetime.utcnow().isoformat()}

    send_to_kafka('results', kafka_msg)
