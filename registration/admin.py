from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.Question)
admin.site.register(models.Response)

class InducteesAdmin(admin.ModelAdmin):
    list_display = ('user','rollnumber','department','is_club_member','profile_picture','full_name','phone_number','year')
    list_filter = ('is_club_member','year')

admin.site.register(models.Inductees,InducteesAdmin)

@admin.register(models.Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('user','comment','date','status','round','by','year')
    list_filter = ('round','status','year','date')
    search_fields = ('user__user__username','user__rollnumber','user__department','user__full_name','user__phone_number','comment','by')
