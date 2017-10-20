from django.conf.urls import url
from .views import base, receiver

urlpatterns = [
	url(r'^$', base),
	url(r'^receiver/', receiver),
]