# rights/admin.py

from django.contrib import admin
from .models import LegalRight, LegalDocument, DocumentField

@admin.register(LegalRight)
class LegalRightAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'display_tags')
    list_filter = ('category',)
    search_fields = ('title', 'summary', 'category')
    
    def display_tags(self, obj):
        return ', '.join(obj.tags)
    display_tags.short_description = 'Tags'


class DocumentFieldInline(admin.TabularInline):
    model = DocumentField
    extra = 1

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    inlines = [DocumentFieldInline]

admin.site.register(DocumentField)