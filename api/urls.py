from django.urls import path

from .views import RobotView, TableCreatedRobots

app_name = 'api'

urlpatterns = [
    path('robot/', RobotView.as_view(), name='create_robot'),
    path('download-file/', TableCreatedRobots.as_view(), name='download_file'),
]
