from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostPhoto)
admin.site.register(Relationship)
admin.site.register(Comment)


admin.site.register(Photo)
admin.site.register(Hobby)

admin.site.register(Request)
admin.site.register(Follow)
admin.site.register(Follower)