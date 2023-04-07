from django.db import models

from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from utils.models import BaseModel

from django.contrib.auth.base_user import BaseUserManager

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=30)


    objects = CustomUserManager()
    # username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class fyppanel(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.RESTRICT)
    facultyid = models.CharField(max_length=45, unique=True)       
    designation = models.CharField(max_length=45)

class department(BaseModel):
    name = models.CharField(max_length=45, unique=True)
    hod = models.CharField(max_length=45)
    
    def __str__(self):
        return self.name
    

class supervisor(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.RESTRICT)
    name = models.CharField(max_length=45)
    faculty_no = models.CharField(max_length=45, unique=True)
    phone_no = models.CharField(max_length=12)
    field_of_interest = models.CharField(max_length=45)
    department = models.ForeignKey(department, on_delete=models.RESTRICT, default=False)

    def __str__(self):
        return self.name


class project(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    batch = models.CharField(max_length=50)
    grade = models.IntegerField(default=0)
    description = models.TextField()
    status = models.CharField(max_length=45,default="initial")
    domain = models.CharField(max_length=45)
    no_of_group_members = models.IntegerField(default=5)
    supervisor = models.ForeignKey(supervisor, on_delete=models.RESTRICT)
    department = models.ForeignKey(department, on_delete=models.RESTRICT)
     

class milestone(BaseModel):
    milestone_name = models.CharField(max_length=75,unique=True)
    document_submissin_date = models.DateField()
    milestone_defending_date = models.DateField()
    milestone_details = models.CharField(max_length=500)
    fyp_panel = models.ForeignKey(fyppanel, on_delete=models.RESTRICT)
    # project = models.ForeignKey(project, on_delete=models.RESTRICT)


class notification(BaseModel):
    title = models.CharField(max_length=75)
    isactive = models.BooleanField(default=False)
    description = models.CharField(max_length=500)
    createdby = models.ForeignKey(fyppanel, on_delete=models.RESTRICT)
    createdate = models.DateField()
    createtime = models.TimeField()


class teamMember(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.RESTRICT)
    rollno = models.CharField(max_length=50)
    grade = models.IntegerField(default=0,
            validators=[
            MaxValueValidator(200),
            MinValueValidator(0)
        ]
    )
