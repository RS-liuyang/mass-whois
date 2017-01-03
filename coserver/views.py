#from django.shortcuts import render
from django.http import HttpResponse
from coserver.models import qDomain
#from uuid import uuid4
from bulk_update.helper import bulk_update
# Create your views here.

def get_names(request):

    #request_id = str(uuid4())
    ret=''
    for _ in range(0, 21):
        ids = list(qDomain.objects.filter(
                        status=0
                   ).values_list('id', flat=True)[:47])

        names = qDomain.objects.filter(pk__in = ids)

        for name in names:
            name.status = 1
            ret = ret + ',' + name.name

        bulk_update(names, update_fields=['status'])

    if not names:
        return HttpResponse('END')

    return HttpResponse(ret)