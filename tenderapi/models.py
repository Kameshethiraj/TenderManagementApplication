from django.db import models
from django.contrib.auth.models import User  # Assuming you're using the default User model

class Role(models.Model):
    rolename = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.rolename

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}"


class Bidding(models.Model):
    id = models.AutoField(primary_key=True)
    biddingId = models.IntegerField(unique=True)
    projectName = models.CharField(max_length=255, default="Metro Phase V 2024")
    bidAmount = models.FloatField()
    yearsToComplete = models.FloatField()
    dateOfBidding = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")
    bidder = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        # Return the bidder's username or any other relevant string representation
        return f"Bidding {self.biddingId} by {self.bidder.user.username}"
