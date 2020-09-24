from django.contrib import admin
from myblog.models import Article,User,Category,Tag,ArticleComment
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields=('content')
    list_display=['article_id','title','created_time']
    search_fields=['title']
    list_filter=['created_time']

class CommentAdmin(admin.ModelAdmin):
    list_display=['username','body','title']
    search_fields=['title']

admin.site.register(Article,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(ArticleComment,CommentAdmin)

