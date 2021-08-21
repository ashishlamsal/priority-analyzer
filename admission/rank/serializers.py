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
    college = serializers.StringRelatedField()
    program = serializers.StringRelatedField()

    # def get_college(self, obj):
    #     return obj.college.name

    # def get_program(self, obj):
    #     return obj.program.name

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
        fields = [
            "cutoff",
            "cutin",
            "cutoffMarks",
            "cutinMarks",
            "seats",
            "type",
            "college",
            "program",
        ]


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
    # collegeprogram = CollegeProgramSerializer(read_only=True, many=False)

    class Meta:
        model = Addmission
        # fields = ['score', 'rank', 'collegeprogram']
        fields = '__all__'
