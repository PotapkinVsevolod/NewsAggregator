from django.urls import path

from aggregator.views import PostsView


urlpatterns = [
    path('', PostsView.as_view(), name='posts'),
]
