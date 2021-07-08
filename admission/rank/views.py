from rest_framework import viewsets
from rest_framework import permissions

from .serializers import (
    ProgramSerializer,
    CollegeSerializer,
    CollegeProgramSerializer,
    AddmissionSerializer,
)
from .models import Program, College, CollegeProgram, Addmission


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
    serializer_class = AddmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
