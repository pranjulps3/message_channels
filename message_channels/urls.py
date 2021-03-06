from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
import message_channels.settings as settings

urlpatterns = [
	url(r'^chat/', include('chat_messages.urls')),
	url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
