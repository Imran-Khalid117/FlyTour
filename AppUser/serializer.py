from rest_framework import serializers
from .models import ApplicationUser


class ApplicationUserSerializer(serializers.ModelSerializer):
    """
    This class in inherited from serializers.ModelSerializer class.

    Fields to show:
        'id', 'email', 'username'
    Fields not to show:
        'password', 'created_at', 'updated_at', 'is_deleted'
    """

    def __init__(self, *args, **kwargs):
        # Get the context passed during serialization
        fields_to_serialize = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields_to_serialize:
            # Filter the fields based on the scenario
            allowed = set(fields_to_serialize)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ApplicationUser
        fields = ['id', 'email', 'username', 'password', 'created_at', 'updated_at',
                  'is_deleted']
