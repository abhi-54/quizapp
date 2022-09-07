from django.contrib import admin
from .models import Result

class ResultAdmin(admin.ModelAdmin):
  readonly_fields = ['quiz', 'user', 'profile', 'score', 'date', 'date1', 'std', 'result_summary']

admin.site.register(Result, ResultAdmin)