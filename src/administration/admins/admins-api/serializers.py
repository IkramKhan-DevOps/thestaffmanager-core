from src.accounts.models import User
from src.administration.admins.models import ShiftDay, Shift, Employee, Client, Site, Position
from rest_framework import serializers


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            'id', 'name'
        ]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            'id', 'name', 'card_color'
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
            'id', 'user', 'employee_id'
        ]


class ShiftSerializer(serializers.ModelSerializer):
    site = SiteSerializer(many=False, read_only=True)
    client = ClientSerializer(many=False, read_only=True)
    position = PositionSerializer(many=False, read_only=True)

    class Meta:
        model = Shift
        fields = [
            'id', 'start_date', 'end_date', 'start_time', 'end_time', 'client', 'employee', 'site', 'position'
        ]


class ShiftDaySerializer(serializers.ModelSerializer):
    shift = ShiftSerializer(many=False, read_only=True)
    employee = EmployeeSerializer(many=False, read_only=True)

    class Meta:
        model = ShiftDay
        fields = '__all__'
