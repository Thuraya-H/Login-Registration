from django.db import models
import re
from datetime import date

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # First name
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        # Last name
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        # Birthday date

        if postData['bday'] == '':
            errors["bday"] = "The Birthday date is required"
        elif date.today() <= date.fromisoformat(postData['bday']):
            errors["bday"] = "The Birthday date should be in past"
        else:
            today = date.today()
            birthDate_year = date.fromisoformat(postData['bday']).year
            birthDate_month = date.fromisoformat(postData['bday']).month
            birthDate_day = date.fromisoformat(postData['bday']).day
            print (today,)
            print(birthDate_year, birthDate_month, birthDate_day)
            age = today.year - birthDate_year - ((today.month, today.day) < (birthDate_month, birthDate_day))
            print(age)
            print("todat date",date.today().year)
            print("birthday date",date.fromisoformat(postData['bday']).year)
            if age < 13 :
                errors["bday"] = "The user should be at least 13 years old"
        # Email
        arr = self.filter(email = postData['email'])
        if postData['email'] == '':
            errors["email"] = "The Email Adress is required"
        elif arr:
            errors["email"] = "The Email are already exist!"
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):            
                errors['email'] = "Invalid email address!"
        # Password
        if postData['password'] == '':
            errors["password"] = "Enter password!"
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        elif postData['password'] != postData['confirm_pw']:
            errors["password"] = "Passwords don't match"
            
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()