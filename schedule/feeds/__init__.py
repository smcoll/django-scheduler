import datetime, itertools

from django.contrib.sites.models import Site
from django.contrib.syndication.views import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import strip_tags

from schedule.feeds.atom import Feed
from schedule.feeds.icalendar import ICalendarFeed
from schedule.models import Calendar


class UpcomingEventsFeed(Feed):
    feed_id = "upcoming"

    def feed_title(self, obj):
        return "Upcoming Events for %s" % obj.name

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Calendar.objects.get(pk=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        return itertools.islice(obj.occurrences_after(timezone.now()),
            getattr(settings, "FEED_LIST_LENGTH", 10))

    def item_id(self, item):
        return str(item.id)

    def item_title(self, item):
        return item.event.title

    def item_authors(self, item):
        if item.event.creator is None:
            return [{'name': ''}]
        return [{"name": item.event.creator.username}]

    def item_updated(self, item):
        return item.event.updated_on

    def item_content(self, item):
        return "%s \n %s" % (item.event.title, item.event.description)


class CalendarICalendar(ICalendarFeed):

    def items(self):
        cal_id = self.args[1]
        cal = Calendar.objects.get(pk=cal_id)

        return cal.events.all()

    def item_uid(self, item):
        return item.slug

    def item_start(self, item):
        return item.start

    def item_end(self, item):
        return item.end

    def item_summary(self, item):
        return item.title

    def item_created(self, item):
        return item.created_on

    def item_description(self, item):
        return item.description

    def item_location(self, item):
        attr_list = ['venue_name', 'address']
        contact_details = [getattr(item, x) for x in attr_list if getattr(item, x) != '']
        return u'; '.join(contact_details)

    def item_url(self, item):
        """ Return full url including domain """
        current_site = Site.objects.get_current()
        return u'%s%s' % (current_site.domain, item.get_absolute_url())

    def item_description(self, item):
        return strip_tags(item.description)

    def item_contact(self, item):
        attr_list = ['contact', 'phone_number', 'email', 'url']
        contact_details = [getattr(item, x) for x in attr_list if getattr(item, x) != '']
        return u'; '.join(contact_details)

    def item_x_cost(self, item):
        return item.cost

    def item_rrule(self, item):
        """ Examples:

            RRULE:FREQ=YEARLY;BYMONTH=2

            RRULE:FREQ=MONTHLY;UNTIL=20121130T235959Z;BYDAY=4SA
            RRULE:FREQ=MONTHLY;BYDAY=4FR

            RRULE:FREQ=WEEKLY;UNTIL=20120417T235959Z;BYDAY=TU;WKST=MO
            RRULE:FREQ=WEEKLY;BYDAY=WE;WKST=MO
            RRULE:FREQ=WEEKLY;COUNT=4;BYDAY=SA;WKST=MO

            RRULE:FREQ=DAILY;COUNT=3
            RRULE:FREQ=DAILY;UNTIL=20120103;BYDAY=SU

        TODO: add support for Rule.params
        """
        if item.rule:
            rrule_str = 'FREQ=%s' % (item.rule.frequency)
            if item.end_recurring_period:
                rrule_str = u'%s;UNTIL=%s' % (rrule_str, item.end_recurring_period.strftime('%Y%m%dT%H%M%SZ'))
            return rrule_str
        else:
            return ''
        return 'FREQ=YEARLY;BYMONTH=2'