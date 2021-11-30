from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id','username', 'name', 'email', 'password', 'address']
        extra_kwargs = {
            'password':{'write_only': True}
        }



    def create(self, validated_data):
        password= validated_data.pop('password',None) 

        # ** for validated data without password(pop fields)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance