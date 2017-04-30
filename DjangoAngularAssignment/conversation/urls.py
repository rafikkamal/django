from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'conversation'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^connect/(?P<pk>[0-9]+)/$', views.ConversationListView.as_view(), name='conversation_connect'),
    url(r'^connect/message/(?P<pk>[0-9]+)/$', views.ConversationProcessor.as_view(), name='conversation_process'),
    url(r'^connect/message/(?P<pk>[0-9]+)/edit/$', views.ConversationProcessorUpdate.as_view(), name='conversation_process_edit'),
    url(r'^connect/message/(?P<pk>[0-9]+)/delete/$', views.ConversationProcessorDelete.as_view(),
        name='conversation_process_delete'),
    url(r'^connect/message/(?P<pk>[0-9]+)/archive/$', views.ConversationProcessorArchive.as_view(),
        name='conversation_process_archive'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)