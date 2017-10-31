from django.shortcuts import render
from django.db.models import Q
from .forms import MessageForm
from .models import Attachment, MessageImage, Message
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from PIL import Image
from channels import Group
import json
from django.template.loader import render_to_string
from message_channels.settings import MEDIA_ROOT
# Create your views here.


def rebase(request, id):
	if request.method == "POST":
		try:
			recipient = User.objects.get(id=id)
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps({'success':False, 'html':"Recipient not found !"}))
		try:
			recent = int(request.POST.get("recent"))
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps({'success':False, 'html':"recent not grabbed"}))
		mymessages = Message.objects.filter(sender=request.user, recipient=recipient, id__gte=(recent+1))
		tomessages = Message.objects.filter(sender=recipient, recipient=request.user, id__gte=(recent+1))
		messages = tomessages.union(mymessages)
		cnt = messages.count()
		if cnt > 0:
			messages = messages.order_by('timestamp')
			recent = messages[cnt-1].id
		html = ""
		sender = False
		for message in messages:
			if message.sender == request.user:
				sender = True
			else:
				sender = False
			html = html+render_to_string('message_channels/reply.html', {'message':message, 'sender': sender,})
		return HttpResponse(json.dumps({'success':True, 'html':html, 'recent':recent}))
	return HttpResponse(json.dumps({'success':False, 'html':"request method error !"}))


def temp(request):
	user1 = User.objects.all()
	user2 = user1[0]
	user1 = user1[1]
	return render(request, 'message_channels/temp.html', {'user1':user1, 'user2':user2,})

def base(request, id):
	recipient = get_object_or_404(User, id=id)
	form = MessageForm(initial={}, recipient=recipient)
	mymessages = Message.objects.filter(sender=request.user, recipient=recipient)
	tomessages = Message.objects.filter(sender=recipient, recipient=request.user)
	messages = tomessages.union(mymessages)
	last_id = -1
	cnt = messages.count()
	recent = -1
	if cnt>=50:
		messages = messages.order_by('timestamp')[cnt-49:cnt]
		last_id = messages[0].id
		recent = messages[49].id
	else:
		if cnt != 0:
			recent = messages[cnt-1].id
		messages = messages.order_by('timestamp')
	context = {
	'form': form,
	'recipient':recipient,
	'messages':messages,
	'last_id':last_id,
	'recent':recent,
	'is_view':True,
	}
	return render(request, 'message_channels/chat.html', context)

def receiver(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.sender = request.user
			message.message = request.POST.get('message')
			message.save()
			for file in request.FILES.getlist('attachments'):
				try:
					attach = Attachment.objects.create(file = file, user=request.user)
					message.files.add(attach)
				except Exception as e:
					print(e)

			for image in request.FILES.getlist('images'):
				try:
					im = Image.open(image)
					image = MessageImage.objects.create(image = image, user=request.user)
					message.images.add(image)
				except Exception as e:
					print(e)
			message.save()
			recipient_html = render_to_string('message_channels/reply.html', {'message':message, 'sender': False,})
			Group(message.recipient.username).send({
			"text": json.dumps({
			    'html' :recipient_html,
			    'id'   : message.sender.id,
			    'message_id'   : message.id,
			    }),
			})
			sender_html = render_to_string('message_channels/reply.html', {'message':message, 'sender': True,})
			Group(message.sender.username).send({
			"text": json.dumps({
			    'html' :sender_html,
			    'id'   : message.recipient.id,
			    'message_id'  : message.id,
			    }),
			})
			return HttpResponse(json.dumps({'success':True, 'html':""}))
		return HttpResponse(json.dumps({'success':False, 'html':"Invalid Message Form"}))
	return HttpResponse(json.dumps({'success':False, 'html':"Request type error"}))



def load_more(request, id):
	if request.method == "POST":
		try:
			recipient = User.objects.get(id=id)
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps({'success':False, 'html':""}))
		try:
			message_id = int(request.POST.get("message_id"))
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps({'success':False, 'html':""}))
		mymessages = Message.objects.filter(sender=request.user, recipient=recipient, id__lte=(message_id-1))
		tomessages = Message.objects.filter(sender=recipient, recipient=request.user, id__lte=(message_id-1))
		messages = tomessages.union(mymessages)
		last_id = -1
		cnt = messages.count()
		if cnt>=50:
			messages = messages.order_by('timestamp')[cnt-49:cnt]
			last_id = messages[0].id
		else:
			messages = messages.order_by('timestamp')
		html = ""
		sender = False
		for message in messages:
			if message.sender == request.user:
				sender = True
			else:
				sender = False
			html = html+render_to_string('message_channels/reply.html', {'message':message, 'sender': sender,})
		return HttpResponse(json.dumps({'success':True, 'html':html, 'last_id':last_id}))
	return HttpResponse(json.dumps({'success':False, 'html':"request method error !"}))
