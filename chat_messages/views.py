from django.shortcuts import render

# Create your views here.


def base(request):
	return render(request, 'chat.html')

def receiver(request):
	pass