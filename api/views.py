import logging
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile, Photo, CreditTransaction
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer, ProfileDetailSerializer, UnlockedProfileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView

logger = logging.getLogger(__name__)

# Create your views here.

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User '{user.username}' created successfully.")
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            }, status=status.HTTP_201_CREATED)
        logger.error(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {}


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info("User logged out successfully.")
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Fetching profiles, excluding user '{self.request.user.username}'")
        return Profile.objects.exclude(user=self.request.user)

    def get_object(self):
        logger.debug(f"Fetching or creating profile for user '{self.request.user.username}'")
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        if created:
            logger.info(f"New profile created for user '{self.request.user.username}'")
        return profile

    def list(self, request, *args, **kwargs):
        logger.info("Listing user profiles with filters.")

        try:
            user_profile = request.user.profile
            # Ensure the user has a date of birth to filter by
            if user_profile.date_of_birth is None:
                logger.warning(f"User {request.user.username} does not have a date of birth. Returning empty list.")
                return Response([], status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            logger.warning(f"User {request.user.username} does not have a profile. Returning empty list.")
            return Response([], status=status.HTTP_200_OK)

        # Start with a base queryset excluding the current user and profiles without a date of birth
        queryset = Profile.objects.exclude(user=request.user).filter(date_of_birth__isnull=False)

        # Apply gender and age filtering based on the user's profile
        if user_profile.gender:
            if user_profile.gender.lower() == 'male':
                # Show younger females
                queryset = queryset.filter(gender__iexact='Female', date_of_birth__gt=user_profile.date_of_birth)
            elif user_profile.gender.lower() == 'female':
                # Show older males
                queryset = queryset.filter(gender__iexact='Male', date_of_birth__lt=user_profile.date_of_birth)
        else:
            logger.info(f"User {request.user.username} has an incomplete profile. Skipping default gender/age filters.")
            # Return empty if gender is not set, as logic depends on it
            return Response([], status=status.HTTP_200_OK)

        # Additional filters from query parameters
        caste = request.query_params.get('caste')
        religion = request.query_params.get('religion')
        mother_tongue = request.query_params.get('mother_tongue')

        if caste:
            queryset = queryset.filter(caste__iexact=caste)
        if religion:
            queryset = queryset.filter(religion__iexact=religion)
        if mother_tongue:
            queryset = queryset.filter(mother_tongue__iexact=mother_tongue)

        logger.debug(f"Final filtered queryset count: {queryset.count()}")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        logger.info(f"Creating profile for user '{self.request.user.username}'")
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating profile for user '{self.request.user.username}'")
        logger.debug(f"Request data: {request.data}")
        partial = kwargs.pop('partial', True) # Always allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            logger.error(f"Profile update failed for user '{self.request.user.username}': {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        logger.info(f"Profile updated successfully for user '{self.request.user.username}'")
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        images = request.FILES.getlist('photo')

        if not images:
            logger.warning(f"Photo upload failed for user '{request.user.username}': No images provided.")
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Basic validation
        if len(images) > 3:
            logger.warning(f"Photo upload failed for user '{request.user.username}': Too many images.")
            return Response({'error': 'You can upload a maximum of 3 images.'}, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            Photo.objects.create(profile=profile, image=image)
        
        logger.info(f"{len(images)} photos uploaded successfully for user '{request.user.username}'.")
        return Response({'message': 'Photos uploaded successfully'}, status=status.HTTP_201_CREATED)


class ProfileDetailView(APIView):
    """
    Retrieve full profile details for an unlocked profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Check if the user has unlocked this profile
        has_unlocked = CreditTransaction.objects.filter(
            user=request.user,
            profile_unlocked_id=pk,
            action='unlock'
        ).exists()

        if not has_unlocked:
            return Response({'detail': 'You have not unlocked this profile.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileDetailSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class UnlockedProfileListView(APIView):
    """
    List all profiles unlocked by the current user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the IDs of profiles unlocked by the user
        unlocked_profile_ids = CreditTransaction.objects.filter(
            user=request.user,
            action='unlock'
        ).order_by('-transaction_date').values_list('profile_unlocked_id', flat=True)

        # Fetch the profiles
        unlocked_profiles = Profile.objects.filter(pk__in=list(unlocked_profile_ids))
        
        # We need to preserve the order from the transaction log
        preserved_order_profiles = sorted(unlocked_profiles, key=lambda p: list(unlocked_profile_ids).index(p.pk))

        serializer = UnlockedProfileSerializer(preserved_order_profiles, many=True)
        return Response(serializer.data)


class UnlockProfileView(APIView):
    """
    Unlock a profile, creating a credit transaction and deducting credits.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            profile_to_unlock = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user has enough credits
        if request.user.credits < 1:
            return Response({'detail': 'Insufficient credits. You need at least 1 credit to unlock a profile.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the profile is already unlocked to prevent duplicate transactions
        if CreditTransaction.objects.filter(user=request.user, profile_unlocked=profile_to_unlock, action='unlock').exists():
            return Response({'detail': 'Profile already unlocked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct credits from user balance
        request.user.credits -= 1
        request.user.save()

        # Create the transaction record
        CreditTransaction.objects.create(
            user=request.user,
            profile_unlocked=profile_to_unlock,
            action='unlock',
            credits_spent=1
        )

        return Response({
            'detail': 'Profile unlocked successfully.',
            'remaining_credits': request.user.credits
        }, status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
