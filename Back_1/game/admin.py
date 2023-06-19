from django.contrib import admin
from .models import SentenceContent, SyllableContent, WordContent	# 추가

admin.site.register(SentenceContent)
admin.site.register(SyllableContent)
admin.site.register(WordContent)