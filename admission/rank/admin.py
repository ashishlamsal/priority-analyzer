from django.contrib import admin
from .models import College, Program, CollegeProgram, Addmission, District, Zone

# Register your models here.
admin.site.register(College)
admin.site.register(Program)
admin.site.register(CollegeProgram)
admin.site.register(Addmission)
admin.site.register(District)
admin.site.register(Zone)
