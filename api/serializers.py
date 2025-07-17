from rest_framework import serializers
from .models import User, Profile, Photo, CreditTransaction
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone_number=self.validated_data.get('phone_number'),
            credits=20  # Grant 20 free credits on registration
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image']


class ProfileSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual profile view - ensures only profile-specific photos are included
    """
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_photos(self, obj):
        # Explicitly filter photos for this specific profile
        profile_photos = Photo.objects.filter(profile=obj)
        return PhotoSerializer(profile_photos, many=True).data
        
class UnlockedProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Recently Unlocked Profiles' list on the dashboard.
    Provides a summary of the profile.
    """
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'date_of_birth', 'occupation', 'photos']


class CreditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditTransaction
        fields = '__all__' 