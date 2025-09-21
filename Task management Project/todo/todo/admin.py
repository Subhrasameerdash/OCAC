from django.contrib import admin
from .models import TODOO

@admin.register(TODOO)
class TODOOAdmin(admin.ModelAdmin):
    list_display = ('srno', 'title', 'user', 'date')
    search_fields = ('title', 'user__username')
