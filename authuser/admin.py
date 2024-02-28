from django.contrib import admin
from .models import UserProfile
from .models import UserUpgrade
from .models import FeedBack

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserUpgrade)
admin.site.register(FeedBack)