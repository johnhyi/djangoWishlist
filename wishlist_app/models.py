from django.db import models
import re, bcrypt
from datetime import datetime, date

class UserManager(models.Manager):
    def register(self, data):
        errors={}

        if len(data['name']) < 1:
            errors['name'] = 'Name is required'
        elif len(data['name']) < 3:
            errors['name'] = 'Name must have atleast 3 characters'

        if len(data['username']) < 1:
            errors['username'] = 'Username is required'
        elif len(data['username']) < 3:
            errors['username'] = 'Username must have atleast 3 characters'

        if len(data['password']) < 8:
            errors['password'] = 'Password must have atleast 8 characters'
        if data['password'] != data['confirm']:
            errors['confirm'] = 'Confirm password does not match with pasword'
        
        if len(data['date']) < 1:
            errors['date'] = 'Please enter hire date'
        else:
            d = datetime.strptime(data['date'], '%Y-%m-%d')
            if d > datetime.now():
                errors['date'] = 'Please enter a valid a date'
        
        if len(errors) == 0:
            return User.objects.create(
                name = data['name'],
                username = data['username'],
                date = data['date'],
                password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
            )
        else:
            return errors

    def login(self, data):
        errors = {}

        if len(data['username']) < 1:
            errors['username'] = 'Username is required'
        else:
            existing_username = User.objects.filter(username=data['username'])
            if len(existing_username) < 1:
                errors['username'] = 'Username is not in use'

        if len(data['password']) < 8:
            errors['password'] = 'Incorrect password'

        if len(errors) == 0:
            stored_password = existing_username[0].password
            if not bcrypt.checkpw(data['password'].encode(), stored_password.encode()):
                errors['password'] = 'Incorrect Password'
                return errors
            else:
                return existing_username[0]
        else:
            return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    date = models.CharField(max_length=8)

    objects = UserManager()

class ItemManager(models.Manager):
    def produceitem(self, data, user_id):
        print(data)
        if len(data['itemname']) < 2:
            return {'itemname': 'Item must be 2 characters or longer'}
        else:
            return Item.objects.create(
                itemname = data['itemname'],
                user = User.objects.get(id=user_id)
            )

class Item(models.Model):
    itemname = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    additems = models.ManyToManyField(User, related_name='add_item')
    objects = ItemManager()

# Create your models here.
