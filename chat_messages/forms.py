from .models import Message
from django.forms import ModelForm

class MessageForm(ModelForm):

	def __init__(self, *args, **kwargs):
		rec = kwargs.pop('recipient',{})
		initial = kwargs.get('initial', {})
		initial['recipient'] = rec
		kwargs['initial'] = initial
		super(MessageForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Message
		fields = ['recipient']


