import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from users.manager import UserManager
# Create your models here.

def image_uoload_profile_agent(instance,filname):
    imagename,extention =  filname.split(".")
    return "user/%s.%s"%(instance.id,extention)

Role=(
    ('Caissier', 'Caissier'),
    ('ChefAgence', 'ChefAgence'),
)  

class UserAub(AbstractBaseUser,PermissionsMixin):
    firstname = models.CharField(max_length=50,blank=True)
    lastname = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=16,unique=True)
    username = models.CharField(max_length=16,unique=True,null=True)
    email = models.EmailField(max_length=50,blank=True)
    post = models.CharField(max_length=200,null=True)
    role= models.CharField(max_length=30, choices=Role, default='Caissier')
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    number_attempt= models.IntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    def __str__(self): 
        return self.username or "N/A"
    
def image_uoload_profile(instance,filname):
    imagename,extention =  filname.split(".")
    return "user/%s.%s"%(instance.id,extention)    

class Caissier(UserAub):
    image=models.ImageField(upload_to=image_uoload_profile ,null=True)
    def __str__(self): 
        return self.phone 
        
#--------manager -----------
class ChefAgence(UserAub):
    image=models.ImageField(upload_to=image_uoload_profile ,null=True)       
    
class Agence(models.Model):
    AGENCE = models.CharField(max_length=5, unique=True, blank=True, null=True)
    AGENCELIB = models.CharField(max_length=200,blank=True,null=True) 
    TXFRAIS = models.CharField(max_length=200,blank=True,null=True)
    TXCOMMV = models.CharField(max_length=6,blank=True,null=True)
    CLIMIN = models.CharField(max_length=6,blank=True,null=True)
    CLIMAX = models.CharField(max_length=6,blank=True,null=True)
    CLIATTR = models.CharField(max_length=6,blank=True,null=True)
    CLIENT = models.CharField(max_length=6,blank=True,null=True)
    ADRNO = models.CharField(max_length=200,blank=True,null=True)
    VILLE = models.CharField(max_length=100,blank=True,null=True)
    CONNECTE = models.CharField(max_length=3,blank=True,null=True)
    AGCPTA = models.CharField(max_length=100,blank=True,null=True)
    AGCOUR = models.CharField(max_length=100,blank=True,null=True)
    IMPRAVIS = models.CharField(max_length=60,blank=True,null=True)
    IMPRETAT = models.CharField(max_length=60,blank=True,null=True)
    IBATAVIS = models.CharField(max_length=60,blank=True,null=True)
    IBATETAT = models.CharField(max_length=60,blank=True,null=True)
    IBATREL = models.CharField(max_length=60,blank=True,null=True)
    IMPRMATR = models.CharField(max_length=60,blank=True,null=True)
    IBATMATR = models.CharField(max_length=60,blank=True,null=True)
    SYS_CREATED_BY = models.CharField(max_length=60,blank=True,null=True)
    SYS_UPDATED_DATE = models.CharField(max_length=60,blank=True,null=True)
    SYS_UPDATED_BY = models.CharField(max_length=60,blank=True,null=True)
    SYS_VERSION_NUMBER = models.CharField(max_length=60,blank=True,null=True)
    SYS_CREATED_DATE = models.CharField(max_length=60,blank=True,null=True)
    CLIAGP = models.CharField(max_length=60,blank=True,null=True)
    def __str__(self): 
        return self.AGENCELIB or "G/A"

    
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    CODE_RACINE = models.CharField(max_length=6, unique=True, blank=True, null=True)
    CODE_AGENCE = models.ForeignKey(Agence, on_delete=models.CASCADE, to_field='AGENCE',blank=True,null=True)
    NOM = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self): 
        return self.NOM or "C/A"
    
from django.db import models

class DemChq(models.Model):
    CLIENT = models.CharField(max_length=255)
    COMPTE = models.CharField(max_length=255)
    DEVISE = models.CharField(max_length=255)
    RESID = models.CharField(max_length=255)
    NCG = models.CharField(max_length=255)
    LIBELLE = models.CharField(max_length=255)
    NBRCHQ = models.IntegerField()
    TYPCHQ = models.CharField(max_length=255)
    ADRL1 = models.CharField(max_length=255)
    ADRNAT = models.CharField(max_length=255)
    ADRL2 = models.CharField(max_length=255)
    ADRNO = models.CharField(max_length=255)
    ADRL3 = models.CharField(max_length=255)
    ADRL4 = models.CharField(max_length=255)
    ADRL5 = models.CharField(max_length=255)
    DATDEM = models.DateField()
    DATEDDEM = models.DateField()
    DATREDEM = models.DateField()
    DATREMCL = models.DateField()
    DATMAJ = models.DateField()
    REFER1 = models.CharField(max_length=255)
    REFER2 = models.CharField(max_length=255)
    NBRSOU = models.IntegerField()
    CLERIB = models.CharField(max_length=255)
    CHQREM = models.CharField(max_length=255)
    CHQRES = models.CharField(max_length=255)
    ADRL6 = models.CharField(max_length=255)
    INSTR = models.CharField(max_length=255)
    ANNUL = models.CharField(max_length=255)
    DATDES = models.DateField()
    CHQDET = models.CharField(max_length=255)
    STATE = models.CharField(max_length=255)
    VALIDE = models.CharField(max_length=255)
    EXPL = models.CharField(max_length=255)
    XCIRCUL = models.CharField(max_length=255)
    XEXPED = models.CharField(max_length=255)
    CORCLI = models.CharField(max_length=255)
    CORADRNO = models.CharField(max_length=255)
    NSERLOT = models.CharField(max_length=255)
    DELAI = models.CharField(max_length=255)
    NATDEM = models.CharField(max_length=255)
    CREMDEM = models.CharField(max_length=255)
    CREMEFF = models.CharField(max_length=255)
    XAVIS = models.CharField(max_length=255)
    XPRIOR = models.CharField(max_length=255)
    XRENOUV = models.CharField(max_length=255)
    XTOPE = models.CharField(max_length=255)
    EXPLVALID = models.CharField(max_length=255)
    DATVALID = models.DateField()
    NOOPER = models.CharField(max_length=255)
    DADRNO = models.CharField(max_length=255)
    DADRNAT = models.CharField(max_length=255)
    DADRL1 = models.CharField(max_length=255)
    DADRL2 = models.CharField(max_length=255)
    DADRL3 = models.CharField(max_length=255)
    DADRL4 = models.CharField(max_length=255)
    DADRL5 = models.CharField(max_length=255)
    DADRL6 = models.CharField(max_length=255)
    CIRCULANT = models.CharField(max_length=255)
    RENOUVNBR = models.CharField(max_length=255)
    DATHDEM = models.DateField()
    TYPRUE = models.CharField(max_length=255)
    TYPIMM1 = models.CharField(max_length=255)
    TYPIMM2 = models.CharField(max_length=255)
    CODPOST = models.CharField(max_length=255)
    DCODPOST = models.CharField(max_length=255)
    DTYPRUE = models.CharField(max_length=255)
    DTYPIMM1 = models.CharField(max_length=255)
    DTYPIMM2 = models.CharField(max_length=255)
    DNUMRUE = models.CharField(max_length=255)
    NUMRUE = models.CharField(max_length=255)

    class Meta:
        db_table = 'DEMCHQ'  # Nom de la table dans la base de données Oracle

    def __str__(self): 
        return self.CLIENT or "N/A"

def uoload_document(instance, filname):
    extention = os.path.splitext(filname)[1]
    unique_filename = f"{instance.id}{extention}"
    return os.path.join("cheque", unique_filename) 

class UserProfile(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    subj = models.CharField(max_length=100,blank=True, null=True)
    file = models.FileField(upload_to =uoload_document,blank=True, null=True)

class cheque(models.Model):
    numero_de_compte =  models.CharField(max_length=100,blank=True, null=True)
    code_agence = models.CharField(max_length=5,blank=True, null=True)
    Nbre_carnet = models.CharField(max_length=1,blank=True, null=True)
    Nbre_feuilles = models.CharField(max_length=100, blank=True, null=True)
    code_transaction = models.CharField(max_length=2,blank=True, null=True)
    nom_client = models.CharField(max_length=100,blank=True, null=True)
    adresse = models.CharField(max_length=100,blank=True, null=True)
    Code_Devise = models.CharField(max_length=30,blank=True, null=True)
    code_bank = models.CharField(max_length=100,blank=True, null=True)
    code_pays = models.CharField(max_length=10,blank=True, null=True)
    numero_de_debut = models.CharField(max_length=7,blank=True, null=True)

    def __str__(self): 
        return self.numero_de_compte or "N/A"





