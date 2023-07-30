from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'schedules', views.ScheduleViewSet, basename='schedule')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('actualize_schedule/', views.ActualizeSchedule.as_view(), name='actualize_schedule'),
]
