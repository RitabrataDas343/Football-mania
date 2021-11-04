from django.urls import path
from .views import *

app_name = 'teams'

urlpatterns = [
    path('', home, name='home'),
    path('teams/', teams_list, name='teams-list'),
    path('team/create/', TeamCreate.as_view(), name='team-create'),
    path('team/<int:pk>/', TeamUpdate.as_view(), name='team-update'),
    path('team/<int:pk>/delete/', TeamDelete.as_view(), name='team-delete'),
    path('team/<int:team>/players/', players_list, name='players-list'),
    path('team/<int:team>/player/create/', PlayerCreate.as_view(), name='player-create'),
    path('team/<int:team>/player/<slug:slug>/', PlayerUpdate.as_view(), name='player-update'),
    path('team/<int:team>/player/<slug:slug>/delete/', PlayerDelete.as_view(), name='player-delete'),
    path('team/<int:team>/documents/', document_list, name='document-list'),
    path('team/<int:team>/documents/upload', DocumentUpload.as_view(), name='documents-upload'),
    path('team/<int:team>/document/<int:pk>/delete/',DocumentDelete.as_view(), name='document-delete'),
]
