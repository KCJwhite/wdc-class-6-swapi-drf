from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()

# second step: working with Viewsets
# router.register('people', views.PeopleViewSet, base_name='people')

# third step: working with ModelViewsets
router.register('people', views.PeopleModelViewSet, base_name='people')

urlpatterns = [
    # first step: working with raw APIViews
    # path('people/<int:people_id>/', views.PeopleDetailApiView.as_view()),
    # path('people', views.PeopleListApiView.as_view()),
]

urlpatterns += router.urls
