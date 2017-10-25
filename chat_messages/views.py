from django.shortcuts import render
from django.db.models import Q
from .forms import MessageForm
from .models import Attachment, MessageImage
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
	context = {
	'form': form,
	'recipient':recipient,
	}
	return render(request, 'chat.html', context)

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
			recipient_html = render_to_string('reply.html', {'message':message, 'sender': False,})
			Group(message.recipient.username).send({
			"text": json.dumps({
			    'html' :recipient_html,
			    }),
			})
			sender_html = render_to_string('reply.html', {'message':message, 'sender': True,})
			Group(message.sender.username).send({
			"text": json.dumps({
			    'html' :sender_html,
			    }),
			})
			return HttpResponse("successful")
		return HttpResponse("successful")
	return HttpResponse("successful")