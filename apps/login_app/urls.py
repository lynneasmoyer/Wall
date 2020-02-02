from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^user/register$', views.register),
    url(r'^user/login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wall$', views.wall),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment/(?P<message_id>\d+)$', views.post_comment),
    url(r'^delete/(?P<message_id>\d+)$', views.delete)
]