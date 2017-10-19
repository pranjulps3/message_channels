from django.contrib import admin
from .models import Message, MessageImage, Attachment
# Register your models here.
admin.site.register(Message)
admin.site.register(MessageImage)
admin.site.register(Attachment)