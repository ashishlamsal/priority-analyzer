from .models import Program, College, CollegeProgram, Addmission
from rest_framework import serializers


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = ['code', 'name']


class CollegeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = College
        fields =  ['code', 'name']


class CollegeProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CollegeProgram
        fields = '__all__'


class AddmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Addmission
        fields = '__all__'
