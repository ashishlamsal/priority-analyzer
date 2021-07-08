from django.urls import include, path
from rest_framework import routers
from . import views
from . import routes

router = routers.DefaultRouter()
router.register(r"programs", views.ProgramViewSet)
router.register(r"colleges", views.CollegeViewSet)
router.register(r"collegeprograms", views.CollegeProgramViewSet)
router.register(r"admissions", views.AddmissionViewSet)
# router.register(r'prediction', routes.Prediction)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("prediction", routes.Prediction.as_view()),
]
