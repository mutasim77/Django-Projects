from django.contrib import admin
from base.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')  # display by name and surname;
    list_filter = ('username',)  # added filter on a last_name
    search_fields = ('username__startswith', 'username')


# Register your models here.
admin.site.register(User, UserAdmin)
