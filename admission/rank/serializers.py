from .models import Program, College, CollegeProgram, Addmission
from rest_framework import serializers


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = ["code", "name"]


class CollegeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = College
        fields = ["code", "name"]


class CollegeProgramSerializer(serializers.HyperlinkedModelSerializer):
    cutinMarks = serializers.SerializerMethodField()
    cutoffMarks = serializers.SerializerMethodField()

    def get_cutinMarks(self, obj):
        try:
            score = Addmission.objects.get(collegeprogram=obj, rank=obj.cutin).score
        except Addmission.DoesNotExist:
            score = None
        return score

    def get_cutoffMarks(self, obj):
        try:
            score = Addmission.objects.get(collegeprogram=obj, rank=obj.cutoff).score
        except Addmission.DoesNotExist:
            score = None
        return score

    class Meta:
        model = CollegeProgram
        fields = "__all__"


class CollegeProgramsListSerializer(serializers.HyperlinkedModelSerializer):
    programs = serializers.SerializerMethodField()

    def get_programs(self, obj):
        return {"code": obj["program"], "name": obj["program__name"]}

    class Meta:
        model = CollegeProgram
        fields = [
            "programs",
        ]


class AddmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Addmission
        fields = "__all__"
