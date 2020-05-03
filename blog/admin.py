from django.contrib import admin
from .models import PostModel, Comment

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'publish_date')
    prepopulated_fields = {"slug": ["title"]}
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(PostModelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'active', 'date')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(CommentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form

admin.site.register(PostModel, PostModelAdmin)
admin.site.register(Comment, CommentAdmin)