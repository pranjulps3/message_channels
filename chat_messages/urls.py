from django.conf.urls import url
from .views import base, receiver, load_more, temp

urlpatterns = [
	url(r'^(?P<id>\d+)/$', base, name = "chat"),
	url(r'^temp/$', temp, name = "temp"),
	url(r'^receiver/$', receiver, name="send_message"),
	url(r'^load_more/(?P<id>\d+)/$', load_more, name = "load_more"),
]