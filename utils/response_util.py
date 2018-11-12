from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class response(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(response, self).__init__(content, **kwargs)
