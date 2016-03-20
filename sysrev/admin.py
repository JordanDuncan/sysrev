from django.contrib import admin
from sysrev.models import *

# Register your models here.
admin.site.register(Researcher)
admin.site.register(Query)
admin.site.register(Paper)
admin.site.register(Review)