from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from users.manager import UserManager
# Create your models here.

def image_uoload_profile_agent(instance,filname):
    imagename,extention =  filname.split(".")
    return "user/%s.%s"%(instance.id,extention)

class UserAub(AbstractBaseUser,PermissionsMixin):
    firstname = models.CharField(max_length=50,blank=True)
    lastname = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=16,unique=True)
    username = models.CharField(max_length=16,unique=True,null=True)
    email = models.EmailField(max_length=50,blank=True)
    post = models.CharField(max_length=200,null=True)
    image=models.ImageField(upload_to=image_uoload_profile_agent ,null=True,blank=True) 
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
    
class Agence(models.Model):
    AGENCE = models.CharField(max_length=5, unique=True, blank=True, null=True)
    AGENCELIB = models.CharField(max_length=200,blank=True,null=True) 
    TXFRAIS = models.CharField(max_length=200,blank=True,null=True)
    TXCOMMV = models.CharField(max_length=6,blank=True,null=True)
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
    IMPRMATR = models.CharField(max_length=60,blank=True,null=True)
    IBATMATR = models.CharField(max_length=60,blank=True,null=True)
    SYS_CREATED_BY = models.CharField(max_length=60,blank=True,null=True)
    SYS_UPDATED_DATE = models.CharField(max_length=60,blank=True,null=True)
    SYS_UPDATED_BY = models.CharField(max_length=60,blank=True,null=True)
    SYS_VERSION_NUMBER = models.CharField(max_length=60,blank=True,null=True)
    SYS_CREATED_DATE = models.CharField(max_length=60,blank=True)
    CLIAGP = models.CharField(max_length=60,blank=True,null=True)
    def __str__(self): 
        return self.AGENCELIB or "G/A"
    
class Client(models.Model):
    CODE_RACINE = models.CharField(max_length=6, unique=True, blank=True, null=True)
    CODE_AGENCE = models.ForeignKey(Agence, on_delete=models.CASCADE, blank=True, null=True)
    NOM = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self): 
        return self.CODE_RACINE or "C/A"
    
class Demchq(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='demchq') 
    compte = models.CharField(max_length=11,blank=True)
    devise = models.CharField(max_length=4,blank=True)
    resid = models.CharField(max_length=2,blank=True)
    ncg = models.CharField(max_length=6,blank=True)
    libelle = models.CharField(max_length=200,blank=True)
    nbrchq = models.CharField(max_length=2,blank=True)
    typchq = models.CharField(max_length=4,blank=True)
    adrl1 = models.CharField(max_length=200,blank=True)
    adrnat = models.CharField(max_length=4,blank=True)
    adrl2 = models.CharField(max_length=200,blank=True)
    adrno = models.CharField(max_length=4,blank=True)
    adrl3 = models.CharField(max_length=200,blank=True)
    adrl4 = models.CharField(max_length=200,blank=True)
    adrl5 = models.CharField(max_length=200,blank=True)
    datdem = models.DateField(blank=True)
    datedem = models.DateField(blank=True)
    datredem = models.DateField(blank=True)
    datremcl = models.DateField(blank=True)
    datemaj = models.DateField(blank=True)
    datedem = models.DateField(blank=True)
    refer1 = models.CharField(max_length=60,blank=True)
    refer2 = models.CharField(max_length=60,blank=True)
    nbrsou = models.CharField(max_length=100,blank=True)
    clerib = models.CharField(max_length=100,blank=True)
    chqrem = models.CharField(max_length=100,blank=True)
    chqers = models.CharField(max_length=100,blank=True)
    adrl6 = models.CharField(max_length=100,blank=True)
    instr = models.CharField(max_length=100,blank=True)
    annul = models.CharField(max_length=100,blank=True)
    datdes = models.DateField(blank=True)
    chqdet = models.CharField(max_length=10,blank=True)
    state = models.CharField(max_length=10,blank=True)
    valide = models.CharField(max_length=10,blank=True)
    expl = models.CharField(max_length=10,blank=True)
    xcircul = models.CharField(max_length=10,blank=True)
    xexped = models.CharField(max_length=10,blank=True)
    corcli = models.CharField(max_length=10,blank=True)
    coradrno = models.CharField(max_length=10,blank=True)
    nserlot = models.CharField(max_length=10,blank=True)
    delai = models.CharField(max_length=10,blank=True)
    natdem = models.CharField(max_length=10,blank=True)
    cremdem = models.CharField(max_length=10,blank=True)
    cremeff = models.CharField(max_length=10,blank=True)
    xavis = models.CharField(max_length=10,blank=True)
    xprior = models.CharField(max_length=10,blank=True)
    xrenouv = models.CharField(max_length=10,blank=True)
    xtope = models.CharField(max_length=10,blank=True)
    explvalid = models.CharField(max_length=10,blank=True)
    datvalid = models.DateField(blank=True)
    nooper = models.CharField(max_length=7,blank=True)
    dadrno = models.CharField(max_length=100,blank=True)
    dadrnat = models.CharField(max_length=100,blank=True)
    dadrl1 = models.CharField(max_length=100,blank=True)
    dadrl2 = models.CharField(max_length=100,blank=True)
    dadrl3 = models.CharField(max_length=100,blank=True)
    dadrl4 = models.CharField(max_length=100,blank=True)
    dadrl5 = models.CharField(max_length=100,blank=True)
    dadrl6 = models.CharField(max_length=100,blank=True)
    circuilant = models.CharField(max_length=100,blank=True)
    renouvembr = models.CharField(max_length=100,blank=True)
    dathdem = models.DateField(blank=True)
    typrue = models.CharField(max_length=100,blank=True)
    typimm2 = models.CharField(max_length=100,blank=True)
    codpost = models.CharField(max_length=100,blank=True)
    dcodpost = models.CharField(max_length=100,blank=True)
    dtyprue = models.CharField(max_length=100,blank=True)
    dtypimm1 = models.CharField(max_length=100,blank=True)
    dtypimm2 = models.CharField(max_length=100,blank=True)
    dnumrue = models.CharField(max_length=100,blank=True)
    numrue = models.CharField(max_length=100,blank=True)

    def __str__(self): 
        return self.client or "N/A"






    
    









