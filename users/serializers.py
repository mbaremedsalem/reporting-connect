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
        



## register Etudiant 
class RegisterCaissierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caissier
        fields = ('id', 'phone','firstname','lastname','username','post','email', 'password','role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class RegisterChefAgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefAgence
        fields = ('id', 'phone','firstname','lastname','username','post','email', 'password','role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('name', 'subj','file')   
class UserProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    subj = serializers.CharField()
    file = serializers.FileField()             
 
class chequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = cheque
        # Remplacez 'direction' par 'direction_nom' dans les champs
        fields = ('id','numero_de_compte', 'code_agence', 'Nbre_carnet','Nbre_feuilles','code_transaction', 'nom_client', 'adresse','Code_Devise','code_bank','code_pays','numero_de_debut')        

class DemChqSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemChq
        fields = '__all__'


class MyDemChqSerializerizer(serializers.ModelSerializer):
    class Meta:
        model = DemChq
        fields = ['id', 'COMPTE', 'DEVISE', 'NBRCHQ', 'ADRL1', 'REFER1', 'REFER2', 'DATVALID', 'CLIENT__NOM', 'AGENCE__CODE_AGENCE']

class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = '__all__'        

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  

class DemChqDtlSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemChqDtl
        fields = '__all__'                 

class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'    
#super 
class VotreSerializer(serializers.Serializer):
    id = serializers.CharField()
    compte = serializers.CharField()
    client__code_agence = serializers.CharField()
    nbrchq = serializers.IntegerField()
    refer2 = serializers.CharField()
    refer1 = serializers.CharField()
    nbre_feuiles = serializers.IntegerField()
    code_transaction = serializers.IntegerField()
    libelle = serializers.CharField()
    adrl1 = serializers.CharField()
    datdem = serializers.DateField()
    dateddem = serializers.DateField()
    datredem = serializers.DateField()
    datremcl = serializers.DateField()
    datmaj = serializers.DateField()
    client__nom = serializers.CharField()            

        