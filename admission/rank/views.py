from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .serializers import (
    ProgramSerializer,
    CollegeSerializer,
    CollegeProgramSerializer,
    AddmissionSerializer,
    CollegeProgramsListSerializer,
)
from .models import Program, College, CollegeProgram, Addmission
from .utils import getProbabilityString


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows BE programs to be viewed.
    """

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    pagination_class = None


class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows colleges to be viewed.
    """

    queryset = College.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    serializer_class = CollegeSerializer
    pagination_class = None


class CollegeProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows details of programs within a college to be viewed.
    """

    queryset = CollegeProgram.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = (
        "college",
        "program",
        "type",
    )
    ordering_fields = ("cutoff",)
    serializer_class = CollegeProgramSerializer
    pagination_class = None


class CollegeProgramsListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Api endpoint that gives list of program for given input college
    """

    queryset = CollegeProgram.objects.values("program", "program__name").distinct()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("college",)
    serializer_class = CollegeProgramsListSerializer
    pagination_class = None


class RankFilter(filters.FilterSet):
    min_rank = filters.NumberFilter(field_name="rank", lookup_expr='gte')
    max_rank = filters.NumberFilter(field_name="rank", lookup_expr='lte')

    class Meta:
        model = Addmission
        fields = ["collegeprogram",
                  "collegeprogram__college",
                  "collegeprogram__program",
                  "collegeprogram__type",
                  'min_rank',
                  'max_rank']


class AddmissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows sutdents addmitted to be viewed.
    """

    queryset = Addmission.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = RankFilter
    ordering_fields = (
        "rank",
        "score",
    )
    serializer_class = AddmissionSerializer


class Prediction(APIView):
    """
    API endpoint that predits the result based on rank provided.
    """

    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        """we expect rank, college and faculty filter from the frontend"""

        frontendData = request.data

        if frontendData["college"] == "All" and frontendData["faculty"] == "All":
            query_result = CollegeProgram.objects.all()
        elif frontendData["college"] == "All":
            query_result = CollegeProgram.objects.filter(
                program__code__exact=frontendData["faculty"]
            )
        elif frontendData["faculty"] == "All":
            query_result = CollegeProgram.objects.filter(
                college__code__exact=frontendData["college"]
            )
        else:

            query_result = CollegeProgram.objects.filter(
                college__code__exact=frontendData["college"]
            ).filter(program__code__exact=frontendData["faculty"])

        predictionData = []
        for item in query_result:
            singlePrediction = {
                "college": item.college.code,
                "college_name": item.college.name,
                "program": item.program.code,
                "program_name": item.program.name,
                "type": item.type,
                "probablity": getProbabilityString(
                    int(frontendData["rank"]), item.cutoff, item.seats
                ),
            }
            predictionData.append(singlePrediction)

        return Response(predictionData)


class Analysis(APIView):
    """
    API endpoint that for analysis of students data for a college/program.
    """

    parser_classes = [MultiPartParser]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
        we expect college and year from the front end currently and since we are not
        using year for now we will respond result for one college and all faculty
        """
        frontendData = request.data
        if frontendData["college"] == "All" and frontendData["faculty"] != "All":
            lowestRank = -1
            resposeData = []
            resposeData = []
            query_result = CollegeProgram.objects.filter(
                program__code__exact=frontendData["faculty"]
            )

            for college_program in query_result:
                """determine lowest, highest and no of seat for each faculty"""
                program_code = college_program.program.code
                cutoff = college_program.cutoff
                seats = college_program.seats
                type = college_program.type
                lowestRank = college_program.cutin
                college = college_program.college.code

                program_name = college_program.program.name
                college_name = college_program.college.name

                """10 ota leko xa coz tyo rank nai navako data ni raxa database maa so euta
                matra liyo vane tineru suru maa aauod raxa so 10 ota nikalera rank none xa ki
                xaina check garera garnu parne vayo aile ko laagi"""
                # rankSortedQuery = (
                #     Addmission.objects.filter(
                #         collegeprogram__program__code__exact=college_program.program.code
                #     )
                #     .filter(collegeprogram__type__exact=type)
                #     .filter(
                #         collegeprogram__college__code__exact=frontendData["college"]
                #     )
                #     .order_by("rank")[:10]
                # )
                # for item in rankSortedQuery:
                #     if item.rank != None:
                #         lowestRank = item.rank
                #         break
                resposeData.append(
                    {
                        "faculty": program_code,
                        "type": type,
                        "lowerLimit": lowestRank,
                        "upperLimit": cutoff,
                        "seats": seats,
                        "college": college,
                        "program_name": program_name,
                        "college_name": college_name,
                    }
                )
            return Response(resposeData)

        if frontendData["college"] == "All" or frontendData["faculty"] != "All":
            print("Filter should be one college and all faculty")
            assert False
        else:
            lowestRank = -1
            resposeData = []
            resposeData = []
            query_result = CollegeProgram.objects.filter(
                college__code__exact=frontendData["college"]
            )

            for college_program in query_result:
                """determine lowest, highest and no of seat for each faculty"""
                program_code = college_program.program.code
                cutoff = college_program.cutoff
                seats = college_program.seats
                type = college_program.type
                program_name = college_program.program.name
                college_name = college_program.college.name
                """10 ota leko xa coz tyo rank nai navako data ni raxa database maa so euta
                matra liyo vane tineru suru maa aauod raxa so 10 ota nikalera rank none xa ki
                xaina check garera garnu parne vayo aile ko laagi"""
                rankSortedQuery = (
                    Addmission.objects.filter(
                        collegeprogram__program__code__exact=college_program.program.code
                    )
                    .filter(collegeprogram__type__exact=type)
                    .filter(
                        collegeprogram__college__code__exact=frontendData["college"]
                    )
                    .order_by("rank")[:10]
                )
                for item in rankSortedQuery:
                    if item.rank is not None:
                        lowestRank = item.rank
                        break
                resposeData.append(
                    {
                        "faculty": program_code,
                        "type": type,
                        "lowerLimit": lowestRank,
                        "upperLimit": cutoff,
                        "seats": seats,
                        "program_name": program_name,
                        "college_name": college_name,
                    }
                )
            return Response(resposeData)
