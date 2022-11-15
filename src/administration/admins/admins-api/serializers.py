from src.accounts.models import User
from src.administration.admins.models import ShiftDay, Shift, Employee, Client, Site
from rest_framework import serializers


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            'id', 'name'
        ]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id', 'name'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username'
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'user'
        ]


class ShiftSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(many=False, read_only=True)
    site = SiteSerializer(many=False, read_only=True)
    client = ClientSerializer(many=False, read_only=True)

    class Meta:
        model = Shift
        fields = [
            'id', 'start_date', 'end_date', 'start_time', 'end_time', 'client', 'employee', 'site'
        ]


class ShiftDaySerializer(serializers.ModelSerializer):
    shift = ShiftSerializer(many=False, read_only=True)

    class Meta:
        model = ShiftDay
        fields = [
            'id', 'shift', 'shift_date'
        ]
