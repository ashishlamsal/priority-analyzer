from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Program, College, CollegeProgram, Addmission
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


def getProbabilityString(rank, cutoff, total_seats):
    """
    rank < cut_off -  40% of total_seat    => very high chance
    rank < cut_off -  10% of total_seat    => high chance
    rank < cut_off +- 10% of total_seat    => Critical
    rank < cut_off +  30% of total_seat    => low
    ELSE                                   => very low

    cutoff represents cutoff of year 2077 and if other data are present,
    may represet average of cutoffs of different year

    """
    print("cutoff", cutoff)
    if rank < cutoff - 0.4 * total_seats:
        return "very high"
    elif rank < cutoff - 0.1 * total_seats:
        return "high"
    elif rank > cutoff - 0.1 * total_seats and rank < cutoff + 0.1 * total_seats:
        return "critical"
    elif rank < cutoff + 0.3 * total_seats:
        return "low"
    else:
        return "very low"


class Prediction(APIView):

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
                "program": item.program.code,
                "type": item.type,
                "probablity": getProbabilityString(
                    int(frontendData["rank"]), item.cutoff, item.seats
                ),
            }
            predictionData.append(singlePrediction)

        return Response(predictionData)
