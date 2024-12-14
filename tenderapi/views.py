from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Role, UserProfile, Bidding
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsBidder, IsApprover
from django.shortcuts import get_object_or_404
from .serializers import BiddingSerializer, RegistrationSerializer



class RegistrationView(APIView):
    permission_classes = [AllowAny]  # Open to all

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user using the username and password
        user = authenticate(username=username, password=password)

        if user:
          
            try:
                user_role = user.userprofile.role  
            except AttributeError:
                user_role = None

            # Generate the refresh token and access token
            refresh = RefreshToken.for_user(user)
            
            # Return the login response with username, role, and tokens
            return Response({
                "username": user.username,
                "role": user_role.rolename if user_role else "No role assigned",  # Ensure role is included
                "access": str(refresh.access_token),
                "refresh_token":str(refresh),
            }, status=status.HTTP_200_OK)
        
        # If authentication fails, return an error response
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class BiddingAddView(APIView):
    permission_classes = [IsAuthenticated, IsBidder]  # Add IsBidder permission here

    def post(self, request):
        # Get the current authenticated user (bidder)
        print("got it yeah")
        bidder = get_object_or_404(UserProfile, user=request.user)

        # Add bidder's username to the request data
        data = request.data.copy()
        data['bidder'] = bidder.id  # Use username instead of ID

        # Create a serializer with the data
        serializer = BiddingSerializer(data=data)

        # Validate and save the new bidding
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListBiddingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the bidAmount from query parameters
        bid_amount = request.query_params.get('bidAmount', None)
        
        if not bid_amount:
            return Response({'msg': 'No bidAmount provided in query parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter biddings based on bidAmount
        # try:
        #     bid_amount = float(bid_amount)
        # except ValueError:
        #     return Response({'msg': 'Invalid bidAmount provided'}, status=status.HTTP_400_BAD_REQUEST)

        biddings = Bidding.objects.filter(bidAmount__gt=bid_amount)
        
        if biddings.exists():
            serializer = BiddingSerializer(biddings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'no data available'}, status=status.HTTP_400_BAD_REQUEST)

        
class UpdateBiddingView(APIView):
    permission_classes = [IsAuthenticated, IsApprover]

    def patch(self, request, pk):
        try:
            # Fetch the bidding object by ID
            bidding = Bidding.objects.get(pk=pk)
        except Bidding.DoesNotExist:
            return Response({'msg': 'No bidder available'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if 'status' is in the request data
        if 'status' not in request.data:
            return Response({'msg': 'No status provided to update'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and update the data
        serializer = BiddingSerializer(bidding, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBiddingView(APIView):
    permission_classes = [IsAuthenticated]  # Authentication required

    def delete(self, request, pk):
        try:
            # Fetch the bidding object by ID
            bidding = Bidding.objects.get(pk=pk)
        except Bidding.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the authenticated user is the creator of the bidding or has the "Approver" role
        user_profile = UserProfile.objects.get(user=request.user)

        if bidding.bidder.user != request.user:
            return Response({'msg': "you don't have permission"}, status=status.HTTP_403_FORBIDDEN)

        # Delete the bidding object
        bidding.delete()
        return Response({'msg': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"msg": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"msg": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"msg": "Failed to log out", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
