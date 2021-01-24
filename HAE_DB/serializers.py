from .models import *
from rest_framework import serializers, viewsets

#crew serializer
class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = crew
        fields = '__all__'
"""
class CrewListSerializer(serializers.ModelSerializer):

    class Meta:
        ID = serializers.IntegerField(read_only=True)
        name = serializers.CharField(read_only=True)
        des = serializers.CharField(read_only=True)
        picture = serializers.ImageField(read_only=True)
        count = serializers.IntegerField(read_only=True, default=0)
"""
#feed serializer
class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = feed
        fields = '__all__'

#feed comment serializer
class FeedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = feed_comment
        fields = '__all__'

#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

#gathering participant serializer
class GatheringParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = gathering_participant
        fields = '__all__'

#gathering serializer
class GatheringSerializer(serializers.ModelSerializer):
    class Meta:
        model = gathering
        fields = '__all__'

#gathering comment serializer
class GatheringCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = gathering_comment
        fields = '__all__'

#accout serializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = '__all__'

#equipment serializer
class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = equipment
        fields = '__all__'

