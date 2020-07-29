import os
from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app_name='ads'

urlpatterns = [
    path('', views.AdListView.as_view(), name='all'),
    path('ad/nnn', views.FormView.as_view(), name='form_view'),
    path('ads/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/create', 
        views.AdCreateView.as_view(success_url=reverse_lazy('ads:all')), name='ad_create'),
    path('ads/<int:pk>/update', 
        views.AdUpdateView.as_view(success_url=reverse_lazy('ads:all')), name='ad_update'),
    path('ads/<int:pk>/delete', 
        views.AdDeleteView.as_view(success_url=reverse_lazy('ads:all')), name='ad_delete'),
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
    path('ad/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='ad_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='ad_comment_delete'),
    path('ad/<int:pk>/favorite',
    	views.AddFavoriteView.as_view(), name='ad_favorite'),
	path('ad/<int:pk>/unfavorite',
	    views.DeleteFavoriteView.as_view(), name='ad_unfavorite'),
]