from django.contrib import admin

from .models import Listing, Agreement, AgreementRequest, UserDefinedList, Review

# Register your models here.

admin.site.register(Listing)
admin.site.register(Agreement)
admin.site.register(AgreementRequest)
admin.site.register(UserDefinedList)
admin.site.register(Review)

