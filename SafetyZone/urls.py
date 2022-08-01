from django.urls import path

from . import views

app_name = "SafetyZone"
urlpatterns = [
    # ex: /polls/
    path('', views.video_feed, name='video_feed'),
    path('api/app/GetOriginalImage', views.org_image, name='org_image'),
    path('api/app/GetPredictedImage', views.predicted_image, name='predicted_image'),
    path('api/app/GetLogs', views.logs, name='logs'),
    path('api/app/Status', views.status, name='status'),
    path('api/app/ReloadParameters', views.reload_parameters, name='reload_parameters'),
    path('api/app/SetByPass', views.set_bypass, name='set_bypass'),
    path('api/app/GetByPass', views.get_bypass, name='get_bypass'),
    path('api/app/ApplicationRestart', views.app_restart, name='app_restart'),
]