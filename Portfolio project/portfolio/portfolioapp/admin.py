from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Fields shown in the table list (no content here)
    list_display = ('id', 'name', 'email', 'subject')

    # Optional improvements
    search_fields = ('name', 'email', 'subject')   # Adds a search bar
    list_filter = ('subject',)                     # Adds filter sidebar