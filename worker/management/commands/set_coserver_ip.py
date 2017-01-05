from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import redis

class Command(BaseCommand):
    help = 'Set Coordinator Server IP configuration'

    def add_arguments(self, parser):
        parser.add_argument('coserver-ip', type=str)

    def handle(self, *args, **options):
        if not options['coserver-ip']:
            raise CommandError('Coordinator Server IP needs to be an IP address')

        coord_ip = options['coserver-ip'].strip()

        redis_con = redis.StrictRedis(host=settings.REDIS_HOST,
                                      port=settings.REDIS_PORT,
                                      db=settings.REDIS_DB)
        redis_con.set('KAFKA_HOST',
                      '%s:9092' % coord_ip)

        redis_con.set('COSERVER_ENDPOINT',
                      'http://%s:8000/coserver/' % coord_ip)