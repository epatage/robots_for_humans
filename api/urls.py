from django.urls import path

from .views import RobotView
app_name = 'api'

urlpatterns = [
    path('robot/', RobotView.as_view(), name='create_robot'),
]
