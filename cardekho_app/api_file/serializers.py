from rest_framework import serializers

class carSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    desc = serializers.CharField()
    active = serializers.BooleanField(read_only=True)
