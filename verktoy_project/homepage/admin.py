from django.contrib import admin

from .models import Listing, Agreement, AgreementRequest

# Register your models here.

admin.site.register(Listing)
admin.site.register(Agreement)
admin.site.register(AgreementRequest)
