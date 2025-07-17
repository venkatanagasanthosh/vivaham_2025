from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    credits = models.PositiveIntegerField(default=0)
    
    # To avoid clashes with the default User model, we'll use a custom related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm
    mother_tongue = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    raasi = models.CharField(max_length=50, blank=True)
    nakshatram = models.CharField(max_length=50, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    fathers_name = models.CharField(max_length=255, blank=True)
    fathers_occupation = models.CharField(max_length=100, blank=True)
    fathers_designation = models.CharField(max_length=100, blank=True)
    mothers_name = models.CharField(max_length=255, blank=True)
    mothers_occupation = models.CharField(max_length=100, blank=True)
    siblings_details = models.TextField(blank=True)
    education = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    salary = models.FloatField(null=True, blank=True)  # Annual salary in Lakhs
    about = models.TextField(blank=True)

    def __str__(self):
        return self.full_name or self.user.username


class Photo(models.Model):
    profile = models.ForeignKey(Profile, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_photos/')

    def __str__(self):
        return f"Photo for {self.profile.full_name}"

class CreditTransaction(models.Model):
    ACTION_CHOICES = [
        ('unlock', 'Unlock Profile'),
        ('purchase', 'Purchase Credits'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_transactions')
    profile_unlocked = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='unlocked_by')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    credits_spent = models.IntegerField(default=1)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} '{self.action}' on {self.transaction_date.strftime('%Y-%m-%d')}"
