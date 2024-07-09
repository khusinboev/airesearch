from django.contrib import admin
from .models import Alphabet, Author, Soha, Document, LugatSoha, Lugat
from django.contrib.auth.models import User

# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name", "fayl", "sohaID", "miningInfo")

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(LugatSoha)
class LugatSohaAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name", "nameRus", "nameEng")

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(Lugat)
class LugatAdmin(admin.ModelAdmin):
    search_fields = ["wordLatin", "wordKiril"]
    list_display = ("wordLatin", "wordRus", "wordEnglish", "soha")

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(Alphabet)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(Soha)
class SohaAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)

    def save_model(self, request, obj, form, change):
        obj.save()

