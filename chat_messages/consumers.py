from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from urllib.parse import parse_qs
from channels.sessions import channel_session
import json
from channels.auth import channel_session_user, channel_session_user_from_http

# def first_channel(message):
#     print("hello")
#     response = HttpResponse("You Contacted from the location: %s" % message.content['path'])
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)
@channel_session_user_from_http
@channel_session
def message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    Group("chat").send({
        "text": json.dumps({
            'message' :message.content['text'],
            'hull' : "hola",
            }),
    })


@channel_session_user_from_http
@channel_session
def add(message):
    if(message.user.is_authenticated()):
        Group("chat").add(message.reply_channel)
        message.reply_channel.send({ "accept":True })
    else:
        message.reply_channel.send({ "accept":False })


@channel_session_user_from_http
@channel_session
def disconnect(message):
    Group("chat").discard(message.reply_channel)
