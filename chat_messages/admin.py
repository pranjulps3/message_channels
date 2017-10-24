from django.contrib import admin
from .models import Message, ChatProfile, MessageImage, Attachment

admin.site.register(Message)
admin.site.register(ChatProfile)
admin.site.register(MessageImage)
admin.site.register(Attachment)