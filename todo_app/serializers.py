from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    # tags = serializers.CharField(required=False)
    user = serializers.StringRelatedField(read_only=True)  # Display the username

    class Meta:
        model = Todo
        fields = "__all__"

    def create(self, validated_data):
        due_date = validated_data.get("due_date", None)
        timestamp = validated_data.get("timestamp", None)
        # tags = validated_data.pop('tags', [])

        if due_date and timestamp and due_date < timestamp:
            raise serializers.ValidationError(
                "Due date cannot be earlier than the timestamp"
            )

        # Convert list to comma-separated string before saving
        # validated_data['tags'] = ', '.join(tags)
        return Todo.objects.create(**validated_data)

    # tags = serializers.ListField(child=serializers.CharField(), required=False)
    # def update(self, instance, validated_data):
    #     # Convert list to comma-separated string before saving
    #     tags = validated_data.pop('tags', [])
    #     instance.tags = ', '.join(tags)
    #     return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Convert tags from comma-separated string back to a list when retrieving"""
        representation = super().to_representation(instance)
        representation["tags"] = instance.tags.split(", ") if instance.tags else []
        return representation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user
