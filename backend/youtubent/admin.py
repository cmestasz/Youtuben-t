from django.contrib import admin
from .models import CachedAudio, Account, AccountAudio, Session

# Register your models here.
admin.site.register(CachedAudio)
admin.site.register(Account)
admin.site.register(AccountAudio)
admin.site.register(Session)