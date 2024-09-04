# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import MileageRecord


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Additional field to confirm password, not part of the User model
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def validate(self, attrs):
        """
        Custom validation to ensure both password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise ValidationError({'password2': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Overridden create method to handle user creation.
        """
        
        validated_data.pop('password2', None)

        
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data.get('role', User.Role.CONSUMER)  
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']

class UserPayPalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['paypal_address']


class MileageRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageRecord
        fields = ['current_mileage', 'next_change_mileage', 'created_at']
        read_only_fields = ['next_change_mileage', 'created_at']

    def create(self, validated_data):
        # Automatically calculate the next oil change mileage using the model's save method
        mileage_record = MileageRecord(
            user=self.context['request'].user,
            current_mileage=validated_data['current_mileage']
        )
        mileage_record.save()  # This will trigger the save method in the model which calculates the next_change_mileage
        mileage_record.delete_unnecessary_mileage()  # Optional: Delete unnecessary mileage records
        return mileage_record