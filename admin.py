from django.contrib.gis.db import models
from django.utils.html import format_html
from django.contrib.gis import admin
from django.db.models import Count
from diana.utils import get_fields, DEFAULT_FIELDS, DEFAULT_EXCLUDE
from admin_auto_filters.filters import AutocompleteFilter
from .models import *
from django.conf import settings
from PIL import Image as ima


class AuthorFilter(AutocompleteFilter):
    title = 'Author' # display title
    field_name = 'authors' # name of the foreign key field

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Author, exclude=DEFAULT_EXCLUDE)
    search_fields = ['name', 'surname', 'formatted_name']

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):

    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Work, exclude=DEFAULT_EXCLUDE)
    list_display = ['short_title', 'title', 'modernized_title', 'get_author_list']
    autocomplete_fields = ['authors']
    search_fields = ['title', 'authors__name'] 
    list_filter = [AuthorFilter]

    def get_author_list(self, obj):
        return "\n".join([author.name for author in obj.authors.all()])

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'uuid', *DEFAULT_FIELDS]
    fields = get_fields(Page, exclude=DEFAULT_EXCLUDE + ['text_vector'])
    list_display = ['number', 'work',]
    search_fields = ['id', 'work__name', 'number']
    autocomplete_fields = ['work']


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):

    readonly_fields = ['id', 'size', *DEFAULT_FIELDS]
    fields = get_fields(Cluster, exclude=DEFAULT_EXCLUDE)
    list_display = ['__str__', 'size',]
    search_fields = ['id']


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):

    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Segment, exclude=DEFAULT_EXCLUDE)
    autocomplete_fields = ['page', 'cluster']


@admin.register(Graphics)
class GraphicsModel(admin.ModelAdmin):

    fields              = ['image_preview', *get_fields(Graphics, exclude=['id'])]
    readonly_fields     = ['iiif_file', 'uuid', 'image_preview', *DEFAULT_FIELDS]
    list_display        = ['thumbnail_preview', 'work', 'label_sv']
    search_fields       = ['label_sv', 'label_en', 'work']
    autocomplete_fields = ['work', 'page']
    
    list_per_page = 10

    def image_preview(self, obj):
        return format_html(f'<img src="{settings.IIIF_URL}{obj.iiif_file}/full/full/0/default.jpg" height="300" />')

    def thumbnail_preview(self, obj):
        return format_html(f'<img src="{settings.IIIF_URL}{obj.iiif_file}/full/full/0/default.jpg" height="100" />')
