from django.contrib import admin
from .models import College, Program, CollegeProgram, addmission

# Register your models here.
admin.site.register(College)
admin.site.register(Program)
admin.site.register(CollegeProgram)
admin.site.register(addmission)
