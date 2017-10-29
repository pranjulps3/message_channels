from django import template
from django.conf import settings
from chat_messages.forms import MessageForm
from chat_messages.models import Message

register = template.Library()

def get_message(message, user):
	sender = False
	if message.sender == user:
		sender = True
	return {
	'message':message,
	'sender':sender,
	}

def get_chatbox(request,recipient):
	form = MessageForm(initial={}, recipient=recipient)
	mymessages = Message.objects.filter(sender=request.user, recipient=recipient)
	tomessages = Message.objects.filter(sender=recipient, recipient=request.user)
	messages = tomessages.union(mymessages)
	last_id = -1
	cnt = messages.count()
	if cnt>=50:
		messages = messages.order_by('timestamp')[cnt-50:cnt]
		last_id = messages[0].id
	else:
		messages = messages.order_by('timestamp')
	return {
	'form': form,
	'request':request,
	'recipient':recipient,
	'messages':messages,
	'last_id':last_id,
	}


def get_headers():
	return {}

def get_footers():
	return {}

register.inclusion_tag('message_channels/reply.html')(get_message)
register.inclusion_tag('message_channels/headers.html')(get_headers)
register.inclusion_tag('message_channels/footers.html')(get_footers)
register.inclusion_tag('message_channels/chat.html')(get_chatbox)