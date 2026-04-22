from django.contrib import admin

from ..models import Profile


class ProfileInline(admin.StackedInline):
    fk_name = "usuario"

    model = Profile

    extra = 0

    min_num = 1

    can_delete = False
