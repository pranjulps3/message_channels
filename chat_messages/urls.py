from django.conf.urls import url
from .views import base, receiver

urlpatterns = [
	url(r'^(?P<id>\d+)$', base),
	url(r'^receiver/', receiver, name="send_message"),
]