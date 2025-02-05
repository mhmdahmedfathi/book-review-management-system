from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            is_active=validated_data.get('is_active', True)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("User not found or email is incorrect")
            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return {
                    'user': user,
                    'token': token.key
                }
            else:
                raise serializers.ValidationError("Incorrect password")
        else:
            raise serializers.ValidationError("Email and password are required")

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']