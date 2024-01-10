from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Documentation

# Register your models here.

admin.site.register(Documentation, SimpleHistoryAdmin)