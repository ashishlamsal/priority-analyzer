from django.contrib import admin
from .models import College, Program, CollegeProgram, Addmission

# Register your models here.
admin.site.register(College)
admin.site.register(Program)
admin.site.register(CollegeProgram)
admin.site.register(Addmission)
