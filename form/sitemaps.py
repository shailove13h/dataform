from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from blog.models import Category, Post

class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()

class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.filter(status=Post.ACTIVE)
    
    def lastmod(self, obj):
        return obj.created_at
    

class ManualSitemap(Sitemap):
    def items(self):
        return [
            {'url': reverse('blog'), 'changefreq': 'weekly', 'priority': 0.5},
            {'url': reverse('about'), 'changefreq': 'yearly', 'priority': 0.3},
            # Add more objects here as needed
        ]

    def location(self, item):
        return item.get('url')

    def lastmod(self, item):
        # return the last modification time of the item, if applicable
        pass

    def changefreq(self, item):
        return item.get('changefreq', 'weekly')

    def priority(self, item):
        return item.get('priority', 0.5)