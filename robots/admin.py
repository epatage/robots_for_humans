from django.contrib import admin

from .models import Robot, RobotModel


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = (
        'serial',
        'model',
        'version',
        'created',
        'sold',
        'id'
    )
    search_fields = ('serial', 'model', 'version', 'created')
    list_filter = ('model', 'created')
    list_editable = ('model', 'version', 'created', 'sold')


@admin.register(RobotModel)
class RobotModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    search_fields = ('name',)
    list_filter = ('name',)
