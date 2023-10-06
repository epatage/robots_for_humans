from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'robot_serial', 'purchase')
    search_fields = ('email', 'robot_serial')
    list_filter = ('robot_serial',)
    list_editable = ('robot_serial', 'purchase')
