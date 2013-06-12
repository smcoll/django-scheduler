from django.contrib import admin

from schedule.models import Calendar, Event, CalendarRelation, Rule


class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event, EventAdminOptions)
admin.site.register([Rule, CalendarRelation])