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
    
class Demchq(models.Model):
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE,to_field='CODE_RACINE',blank=True,null=True) 
    COMPTE = models.CharField(max_length=11,blank=True, null=True)
    DEVISE = models.CharField(max_length=4,blank=True, null=True)
    RESID = models.CharField(max_length=2,blank=True, null=True)
    NCG = models.CharField(max_length=6,blank=True, null=True)
    LIBELLE = models.CharField(max_length=200,blank=True, null=True)
    NBRCHQ = models.CharField(max_length=2,blank=True, null=True)
    TYPCHQ = models.CharField(max_length=4,blank=True, null=True)
    ADRL1 = models.CharField(max_length=200,blank=True, null=True)
    ADRNAT = models.CharField(max_length=4,blank=True, null=True)
    ADRL2 = models.CharField(max_length=200,blank=True, null=True)
    ADRNO = models.CharField(max_length=4,blank=True, null=True)
    ADRL3 = models.CharField(max_length=200,blank=True, null=True)
    ADRL4 = models.CharField(max_length=200,blank=True, null=True)
    ADRL5 = models.CharField(max_length=200,blank=True, null=True)
    DATDEM = models.DateField(blank=True, null=True)
    DATEDDEM = models.DateField(blank=True, null=True)
    DATREDEM = models.DateField(blank=True, null=True)
    DATREMCL = models.DateField(blank=True, null=True)
    DATMAJ = models.DateField(blank=True, null=True)
    REFER1 = models.CharField(max_length=60,blank=True, null=True)
    REFER2 = models.CharField(max_length=60,blank=True, null=True)
    NBRSOU = models.CharField(max_length=100,blank=True, null=True)
    CLERIB = models.CharField(max_length=100,blank=True, null=True)
    CHQREM = models.CharField(max_length=100,blank=True, null=True)
    CHQRES = models.CharField(max_length=100,blank=True, null=True)
    ADRL6 = models.CharField(max_length=100,blank=True, null=True)
    INSTR = models.CharField(max_length=100,blank=True, null=True)
    ANNUL = models.CharField(max_length=100,blank=True, null=True)
    DATDES = models.DateField(blank=True, null=True)
    CHQDET = models.CharField(max_length=10,blank=True, null=True)
    STATE = models.CharField(max_length=10,blank=True, null=True)
    VALIDE = models.CharField(max_length=10,blank=True, null=True)
    EXPL = models.CharField(max_length=10,blank=True, null=True)
    XCIRCUL = models.CharField(max_length=10,blank=True, null=True)
    XEXPED = models.CharField(max_length=10,blank=True, null=True)
    CORCLI = models.CharField(max_length=10,blank=True, null=True)
    CORADRNO = models.CharField(max_length=10,blank=True, null=True)
    NSERLOT = models.CharField(max_length=10,blank=True, null=True)
    DELAI = models.CharField(max_length=10,blank=True, null=True)
    NATDEM = models.CharField(max_length=10,blank=True, null=True)
    CREMDEM = models.CharField(max_length=10,blank=True, null=True)
    CREMEFF = models.CharField(max_length=10,blank=True, null=True)
    XAVIS = models.CharField(max_length=10,blank=True, null=True)
    XPRIOR = models.CharField(max_length=10,blank=True, null=True)
    XRENOUV = models.CharField(max_length=10,blank=True, null=True)
    XTOPE = models.CharField(max_length=10,blank=True, null=True)
    EXPLVALID = models.CharField(max_length=10,blank=True, null=True)
    DATVALID = models.DateField(blank=True, null=True)
    NOOPER = models.CharField(max_length=7,blank=True, null=True)
    DADRNO = models.CharField(max_length=100,blank=True, null=True)
    DADRNAT = models.CharField(max_length=100,blank=True, null=True)
    DADRL1 = models.CharField(max_length=100,blank=True, null=True)
    DADRL2 = models.CharField(max_length=100,blank=True, null=True)
    DADRL3 = models.CharField(max_length=100,blank=True, null=True)
    DADRL4 = models.CharField(max_length=100,blank=True, null=True)
    DADRL5 = models.CharField(max_length=100,blank=True, null=True)
    DADRL6 = models.CharField(max_length=100,blank=True, null=True)
    CIRCULANT = models.CharField(max_length=100,blank=True, null=True)
    RENOUVNBR = models.CharField(max_length=100,blank=True, null=True)
    DATHDEM = models.DateField(blank=True, null=True)
    TYPRUE = models.CharField(max_length=100,blank=True, null=True)
    TYPIMM1 = models.CharField(max_length=100,blank=True, null=True)
    TYPIMM2 = models.CharField(max_length=100,blank=True, null=True)
    CODPOST = models.CharField(max_length=100,blank=True, null=True)
    DCODPOST = models.CharField(max_length=100,blank=True, null=True)
    DTYPRUE = models.CharField(max_length=100,blank=True, null=True)
    DTYPIMM1 = models.CharField(max_length=100,blank=True, null=True)
    DTYPIMM2 = models.CharField(max_length=100,blank=True, null=True)
    DNUMRUE = models.CharField(max_length=100,blank=True, null=True)
    NUMRUE = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self): 
        return self.LIBELLE or "N/A"


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)

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





