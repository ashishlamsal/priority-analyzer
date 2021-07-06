from rest_framework import viewsets
from rest_framework import permissions

from .serializers import StudentSerializer, ProgramSerializer, CollegeProgramSerializer, CollegeSerializer
from .models import College, Program, CollegeProgram, addmission


class ProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class CollegeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CollegeProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CollegeProgram.objects.all()
    serializer_class = CollegeProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = addmission.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
