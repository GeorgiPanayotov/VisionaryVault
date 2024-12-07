from django.contrib import admin
from .models import Comment, ArtPiece, Category


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'status', 'user', 'art_piece', 'timestamp')
    list_filter = ('status',)  # Filter by the reported status
    actions = ['mark_as_unreported']

    def mark_as_unreported(self, request, queryset):
        queryset.update(status='active')

    mark_as_unreported.short_description = "Mark selected comments as active"

    def mark_as_unreported(self, request, queryset):
        queryset.update(status='active')

    mark_as_unreported.short_description = "Mark selected comments as active"


@admin.register(ArtPiece)
class ArtPieceAdmin(admin.ModelAdmin):
    list_display = ('description', 'status', 'likes_count', 'timestamp')
    list_filter = ('status',)  # Filter by the reported status
    actions = ['mark_as_unreported']

    def mark_as_unreported(self, request, queryset):
        queryset.update(status='active')

    mark_as_unreported.short_description = "Mark selected art pieces as active"

    def delete_art_pieces(self, request, queryset):
        queryset.delete()

    delete_art_pieces.short_description = "Delete selected art pieces"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category', 'description')  # Specify fields to display in the list view
    search_fields = ('category_name',)
