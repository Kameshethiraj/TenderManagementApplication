from rest_framework import serializers
from .models import Bidding,  Role, UserProfile
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['rolename']

class RegistrationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'company_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Extract user data
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        company_name = validated_data['company_name']
        role_name = validated_data['role']

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Find or create the role
        role, _ = Role.objects.get_or_create(rolename=role_name.upper())

        # Create user profile
        UserProfile.objects.create(user=user, company_name=company_name, role=role)

        return user

class BiddingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bidding
        fields = ['id', 'biddingId', 'projectName', 'bidAmount', 'yearsToComplete', 'dateOfBidding', 'status', 'bidder']
