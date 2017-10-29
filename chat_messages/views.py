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
# Create your views here.


def base(request, id):
	recipient = get_object_or_404(User, id=id)
	form = MessageForm(initial={}, recipient=recipient)
	mymessages = Message.objects.filter(sender=request.user, recipient=recipient)
	tomessages = Message.objects.filter(sender=recipient, recipient=request.user)
	messages = tomessages.union(mymessages)
	last_id = -1
	if tomessages.count()>=50:
		messages = messages.order_by('timestamp')[:50]
		last_id = messages[0].id
	messages = messages.order_by('timestamp')
	print(messages)
	context = {
	'form': form,
	'recipient':recipient,
	'messages':messages,
	'last_id':last_id,
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
			return HttpResponse("successful")
		return HttpResponse("unsuccessful")
	return HttpResponse("unsuccessful")

def load_more(request):
	pass