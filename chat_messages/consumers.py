from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from urllib.parse import parse_qs
from channels.sessions import channel_session
import json
from django.contrib.auth.models import User
from chat_messages.models import Message
from channels.auth import channel_session_user, channel_session_user_from_http

# def first_channel(message):
#     print("hello")
#     response = HttpResponse("You Contacted from the location: %s" % message.content['path'])
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)
@channel_session_user
def message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    mes = parse_qs(message.content['text'])
    user = User.objects.get(username = 'user')
    #sender = User.objects.get(username = message.user.username)
    #message = Message.objects.create(sender=sender, recipient = user, message = mes)
    


@channel_session_user_from_http
def add(message):
    if(message.user.is_authenticated()):
        Group(message.user.username).add(message.reply_channel)
        message.reply_channel.send({ "accept":True })
    else:
        message.reply_channel.send({ "accept":False })


@channel_session_user
def disconnect(message):
    Group(message.user.username).discard(message.reply_channel)
