from rest_framework.permissions import BasePermission
from .models import UserProfile, Role

class IsBidder(BasePermission):
    """
    Custom permission to allow access only to users with the 'Bidder' role.
    """

    def has_permission(self, request, view):
        # Get the user profile associated with the authenticated user
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            # Check if the user's role is 'Bidder'
            if user_profile.role and user_profile.role.rolename == 'BIDDER':
                return True
        except UserProfile.DoesNotExist:
            return False
        return False

class IsApprover(BasePermission):
    """
    Custom permission to allow access only to users with the 'Approver' role.
    """

    def has_permission(self, request, view):
        # Get the user profile associated with the authenticated user
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            # Check if the user's role is 'Approver'
            if user_profile.role and user_profile.role.rolename == 'APPROVER':
                return True
        except UserProfile.DoesNotExist:
            return False
        return False
