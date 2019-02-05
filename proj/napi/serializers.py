import re
from rest_framework import serializers
from napi.models import ProcessQueueAction, Tasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'name', 'task_id')


class ProcessQueueActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='pq-detail', lookup_field='tracking_id')
    tasks = TaskSerializer(many=True, required=False, read_only=True)
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = ProcessQueueAction
        fields = ('url', 'name', 'tracking_id', 'gender', 'type', 'remarks',
                  'citizen_number', 'phone', 'owner', 'created', 'tasks' )
        read_only_fields = ('tracking_id', 'tasks')

    def validate_citizen_number(self, value):
        """
        Check that citizen_number is a valid citizen number
        """
        citizen_number_pattern = r"(.*)(\d{5}[-.$_ +]?\d{7}[-.$_ +]?\d{1})"

        if not re.match(citizen_number_pattern, str(value)):
            raise serializers.ValidationError("A valid citizen number is required")

        return value

    def validate_phone(self, value):
        """
        Check that the phone number is valid.
        """

        if str(value)[:2] != '92':
            raise serializers.ValidationError("Phone number should start with 92")
        if len(str(value)) != 12:
            raise serializers.ValidationError("Phone number should be 12 numbers long")
        return value



