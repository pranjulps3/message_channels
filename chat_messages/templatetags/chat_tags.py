from django import template
from django.conf import settings

register = template.Library()

def get_message(message, user):
	sender = False
	if message.sender == user:
		sender = True
	return {
	'message':message,
	'sender':sender,
	}


register.inclusion_tag('message_channels/reply.html')(get_message)