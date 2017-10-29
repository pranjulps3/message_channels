from django.conf.urls import url
from .views import base, receiver, load_more

urlpatterns = [
	url(r'^(?P<id>\d+)/$', base, name = "chat"),
	url(r'^receiver/$', receiver, name="send_message"),
	url(r'^load_more/(?P<id>\d+)/$', load_more, name = "load_more"),
]