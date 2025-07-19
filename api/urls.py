from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileViewSet, PhotoUploadView,
    UnlockedProfileListView, ProfileDetailView, UnlockProfileView, UserDetailView,
    DebugEnvironmentView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile URLs
    path('profiles/', ProfileViewSet.as_view({'get': 'list'}), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/unlock/', UnlockProfileView.as_view(), name='profile-unlock'),
    
    # Current User specific URLs
    path('me/profile/', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='profile-me'),
    path('me/profile/upload-photos/', PhotoUploadView.as_view(), name='photo-upload'),
    path('me/unlocked-profiles/', UnlockedProfileListView.as_view(), name='unlocked-profiles-list'),
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Debug endpoint
    path('debug/environment/', DebugEnvironmentView.as_view(), name='debug-environment'),
] 