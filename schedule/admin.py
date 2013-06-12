from django.contrib import admin

from schedule.models import Calendar, Event, EventCategory, CalendarRelation, Rule


class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event, EventAdminOptions)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register([Rule, CalendarRelation])