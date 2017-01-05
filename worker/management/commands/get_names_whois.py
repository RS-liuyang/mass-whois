from random import randint
from time import sleep
from mass_whois.config import get_config

from django.core.management.base import BaseCommand

import requests

def main_loop():
    coserver_endpoint = get_config('COSERVER_ENDPOINT')
        #'http://127.0.0.1:8000/coserver/'
    print 'get data from' + coserver_endpoint


    try:
        resp = requests.get(coserver_endpoint, timeout=120)
    except Exception as exc:
        print exc
        print 'Sleeping for a bit to give the coordinator a break'
        sleep(randint(3, 8))
        return

    if resp.status_code != 200:
        # Coordinator might no be up, try later.
        print 'Got non-HTTP 200 back from coordinator, will try later'
        sleep(5)
        return

    if resp.text.strip().upper() == 'END':
        # No more IPs to work with or the list hasn't finished
        # generating yet
        print 'No more IPs from coordinator, will check back later'
        sleep(30)
        return

    for name in resp.text.split(','):
        print name

    sleep(30)

class Command(BaseCommand):
    help = 'Get names to lookup from coserver'

    def handle(self, *args, **options):
        while True:
            main_loop()
