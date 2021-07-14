from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django_filters import rest_framework as filters

from .serializers import (
    ProgramSerializer,
    CollegeSerializer,
    CollegeProgramSerializer,
    AddmissionSerializer,
)
from .models import Program, College, CollegeProgram, Addmission
from .utils import getProbabilityString


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CollegeProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CollegeProgram.objects.all()
    serializer_class = CollegeProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddmissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Addmission.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('rank', 'collegeprogram', 'collegeprogram__college', 'collegeprogram__program', 'collegeprogram__type')
    serializer_class = AddmissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class Prediction(APIView):

    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

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
                "program": item.program.code,
                "type": item.type,
                "probablity": getProbabilityString(
                    int(frontendData["rank"]), item.cutoff, item.seats
                ),
            }
            predictionData.append(singlePrediction)

        return Response(predictionData)