from django.contrib import admin
from editor_reviews import models

# Register your models here.
@admin.register(models.Editor_Reviews)
class CustomEditor_ReviewsAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Editor_Reviews_Image)
class CustomEditor_Reviews_ImageAdmin(admin.ModelAdmin):
	pass

