from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from accounts.models import User


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    gender = serializers.ChoiceField(choices=User.GenderChoices)
    role = serializers.ChoiceField(choices=User.RoleChoices)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['gender'] = self.validated_data.get('gender', '')
        data['role'] = self.validated_data.get('role', '')

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'gender', 'first_name', 'role', 'phone_number']
