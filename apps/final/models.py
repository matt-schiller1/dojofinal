from django.db import models
import re
import bcrypt
import datetime

# Create your models here.
class UserManager(models.Manager):
  def validation(self, postData):
    errors = {}
    if len(postData['name']) < 3:
      errors['name'] = "Name needs to be at least 3 characters"
    if len(postData['username']) < 3:
      errors['username'] = "Name needs to be at least 3 characters"
    if len(postData['password']) < 8:
      errors['password'] = "Password needs to be at least 8 characters"
    if postData['password'] != postData['cpassword']:
      errors['confirm'] = "Passwords need to match"
    if len(User.objects.filter(username=postData['username'])) > 0:
      errors['unique'] = "Username already exists"
    return errors
  
  def register(self, postData):
    #Hash PW
    hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
    print(hash_pw)
    #call create
    new_user = self.create(name=postData['name'],username=postData['username'], password=hash_pw)
    print("successfully registered", new_user.username)
    return new_user.id

  def login_validation(self, loginData):
    login_user = User.objects.filter(username=loginData['login_user'])
    errors = {}
    if len(login_user) == 0:
      errors['login'] = "Email/Password is incorrect"      
    elif not bcrypt.checkpw(loginData['login_password'].encode(), login_user[0].password.encode()):
      errors['password'] = "Invalid Email Address or Password"
    return errors
  
  def trip_validation(self, postData):
    errors = {}
    if datetime.datetime.strptime(postData['datefrom'], "%Y-%m-%d") > datetime.datetime.strptime(postData['dateto'], "%Y-%m-%d"):
      errors['date'] = "Return date must be later than depart date"
    if datetime.datetime.strptime(postData['datefrom'], "%Y-%m-%d") < datetime.datetime.now():
      errors['datepast'] = "Trips need to be in the future"
    if len(postData['destination']) < 3:
      errors['destination'] = "Destinations must be 3 characters"
    if len(postData['description']) < 3:
      errors['description'] = "Descriptions must be 3 characters"   
    return errors

    

class User(models.Model):
  name = models.CharField(max_length=45)
  username = models.CharField(max_length=20)
  password = models.CharField(max_length=255)
  #trip name created
  #join_trip
  objects = UserManager()

  def __repr__(self):
    return f"<User object: {self.name} ({self.id})>"

class Trip(models.Model):
  destination = models.CharField(max_length=100)
  description = models.TextField()
  datefrom = models.DateField()
  dateto = models.DateField()
  created_by = models.ForeignKey(User, related_name="trip_name")
  join = models.ManyToManyField(User, related_name="join_trip")
  objects = UserManager()

  def __repr__(self):
    return f"<User object: {self.destination} ({self.id})>"