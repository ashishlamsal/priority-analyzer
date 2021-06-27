from .models import College, Program, CollegeProgram, Student
from rest_framework import serializers


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
        # fields = ['url', 'username', 'email', 'groups']


class CollegeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = College
        fields = '__all__'
        # fields = ['url', 'name']

class CollegeProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CollegeProgram
        fields = '__all__'
        # fields = ['url', 'username', 'email', 'groups']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        # fields = ['url', 'name']
