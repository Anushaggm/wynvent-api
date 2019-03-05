from django.contrib import admin

from applications.blog.models import Blog, BlogAuthor, BlogType, TalkToExpert

# admin.site.register(Blog)
admin.site.register(BlogAuthor)
# admin.site.register(BlogType)
admin.site.register(TalkToExpert)
