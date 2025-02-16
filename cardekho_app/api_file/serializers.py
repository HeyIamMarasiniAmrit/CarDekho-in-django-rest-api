from rest_framework import serializers
from ..models import car_list,Showroomlist, Review
from rest_framework.serializers import ValidationError





def alphanumeric(value):
    if not str(value).isalnum():
        raise serializers.ValidationError("Only alphanumeric characters are allowed")


# class carSerializers(serializers.Serializer):
# id = serializers.IntegerField(read_only=True)
# name = serializers.CharField()
# desc = serializers.CharField()
# active = serializers.BooleanField()
# chassisnumber = serializers.CharField(validators=[alphanumeric])
# price = serializers.DecimalField(max_digits=9, decimal_places=2)

# def create(self, validated_data):
#     return car_list.objects.create(**validated_data)
#
# def update(self, instance, validated_data):
#     instance.name = validated_data.get('name', instance.name)
#     instance.desc = validated_data.get('desc', instance.desc)
#     instance.active = validated_data.get('active', instance.active)
#     instance.chassisnumber = validated_data.get('chassisnumber', instance.chassisnumber)
#     instance.price = validated_data.get('price', instance.price)
#     instance.save()
#     return instance
class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('car',)
        fields = "__all__"
class carSerializers(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    Reviews = ReviewSerializers(many=True, read_only=True)
    class Meta:
        model = car_list
        # exclude = ['name']
        fields = "__all__"
        # fields = ['id', 'account_name', 'users', 'created']

    #     custom field
    def get_discounted_price(self,object):
        if object.price is not None:
            discount_price = object.price - 5000
        else:
            discount_price = 5000  # Default value when price is None
        return discount_price

    def validate_price(self, value):
        if value <= 20000.00:
            raise serializers.ValidationError("Price must be greater than 20000.00")
        return value

    def validate(self, data):
        if data['name'] == data['desc']:
            raise serializers.ValidationError("Name and description must be different")
        return data

class ShowroomlistSerializer(serializers.ModelSerializer):

     # showrooms = carSerializers(many=True, read_only=True)
     # showrooms = serializers.StringRelatedField(many=True)
    # showrooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    showrooms = serializers.HyperlinkedRelatedField(
         many=True,
         read_only=True,
         view_name='car_detail'
    )
    class Meta:
        model = Showroomlist
        fields = "__all__"
