from django.contrib import admin

from schedule.models import Calendar, Event, EventCategory, CalendarRelation, Rule


class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventCagtegoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register([Rule, Event, CalendarRelation])