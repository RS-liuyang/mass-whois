from django.core.management.base import BaseCommand, CommandError
import csv
from coserver.models import qDomain

CHUNK_SIZES = 10000

def chunks(l, n):
    """
    Yield successive n-sized chunks from l.

    From: http://stackoverflow.com/a/312464
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]




class Command(BaseCommand):
    help = 'Import top 1m domains csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs = '+')


    def handle(self, *args, **options):
        filename = options['filename'][0]
        print "reading" + filename

        qDomain.objects.all().delete()

        with open(filename) as f:
            reader = csv.reader(f, delimiter=',')
            lr = list(reader)
            for count, lines in enumerate(chunks(lr, CHUNK_SIZES), start=1):
                qDomain.objects.bulk_create([qDomain(ori_id=line[0],name=line[1]) for line in lines])
                print '{:,}'.format(count * CHUNK_SIZES)

        print "file has %d lines" % (count * CHUNK_SIZES)