from django.contrib import admin
from  .models import Contact,Category,Comments,News

class NewAdmin(admin.ModelAdmin):
    list_display = ['title','category','created_at','updated_at','status']
    list_filter = ['category','status']
    prepopulated_fields = {"slug":('title',)}



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','created_at']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','message','created_at']
    list_filter = ['full_name','email','message','created_at']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user','created_at']
    list_filter = ['user','created_at']



admin.site.register(News,NewAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Comments,CommentsAdmin)