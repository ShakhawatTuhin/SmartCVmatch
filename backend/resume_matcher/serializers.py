from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Resume, Bookmark

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'name', 'uploaded_at', 'file', 'parsed_text', 'skills']
        read_only_fields = ['parsed_text', 'skills']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'job_id', 'job_title', 'job_company', 'job_description', 'created_at']
        read_only_fields = ['created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'stats']
        read_only_fields = ['id', 'username']

    def get_stats(self, user):
        try:
            resume_count = Resume.objects.filter(user=user).count()
            bookmark_count = Bookmark.objects.filter(user=user).count()
            return {
                'resume_count': resume_count,
                'bookmark_count': bookmark_count,
            }
        except Exception as e:
            # Return empty stats on error
            return {
                'resume_count': 0,
                'bookmark_count': 0,
                'error': str(e)
            } 