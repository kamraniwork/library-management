from django.contrib.sitemaps import Sitemap
from book.models import Book
from django.urls import reverse


class BookSitemap(Sitemap):
    """
    while change data
    changefreq ={always,hourly,daily,weekly,monthly,yearly,never}

    Importance page
    priority =[0.0 - 1.0]

    protocol ={http,https}

    """
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.created

    def location(self, obj):
        return '/book/%s' % (obj.slug)
