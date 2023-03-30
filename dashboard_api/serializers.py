from rest_framework import serializers
from dashboard.models import CustomUser, SystemData

class SystemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemData
        fields = ['cpu_percent','mem_percent','disk_percent','timestamp','created_at','updated_at']
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'address','username','date_joined']
    date_joined = serializers.SerializerMethodField()
    def get_date_joined(self, obj):
        return obj.date_joined.strftime('%d %B %Y')