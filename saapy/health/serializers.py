from rest_framework import serializers
from .models import Health
from .models import Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [ 'username', 'password']

    def validate_email(self, value):
        # Check that the email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_password(self, value):
        # Check that the password is at least 8 characters long
        if len(value) < 8:
            raise serializers.ValidationError("The password must be at least 8 characters long.")
        return value

class HealthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Health
        fields = ('url', 'timestamp', 'id', 'temperature', 'pulse')
