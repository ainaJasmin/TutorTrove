from django.contrib import admin

# Register your models here.

from . models import *

admin.site.register(Tutor)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(TutorSubject)
admin.site.register(Tutee)
admin.site.register(TuteeHours)
admin.site.register(PaymentStatus)