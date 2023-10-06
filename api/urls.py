from django.urls import path

from .views import OrderView, RobotView, TableCreatedRobots

app_name = 'api'

urlpatterns = [
    path('robot/', RobotView.as_view(), name='create_robot'),
    path('order/', OrderView.as_view(), name='add_order'),
    path('download-file/', TableCreatedRobots.as_view(), name='download_file'),
]
