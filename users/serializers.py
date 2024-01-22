from .models import *
from rest_framework import serializers 
from django.contrib.auth import authenticate
#--------------user serializer-------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserAub
        fields= ('firstname','username','lastname','post','email','phone')

#--------------login---------------------
class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_blocked:
            user.number_attempt=0
            user.save()
            return user
        
        elif user and user.is_active and user.is_blocked:
            # return Response('message')
            # return Response(serializers.errors)
            
            raise serializers.ValidationError({'message':'Compte blocké, veillez contacter equipe informatique'})
        
        try:
            obj= UserAub.objects.get(phone=data['username'])
            if obj.number_attempt<3:
                obj.number_attempt +=1
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké .'})
            else:
                obj.number_attempt +=1
                obj.is_blocked=True
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        except:
            raise serializers.ValidationError({'message':'Informations invalides.'})  
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAub
        fields = ('firstname','username','lastname','post','phone','email','password')
        extra_kwargs = {
            'password': {'write_only': True}
        } 