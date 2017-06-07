from __future__ import unicode_literals

from django.db import models
import datetime
import bcrypt, re
from django.db.models import Q

# Create your models here.

class UserDBManager(models.Manager):
    def hash_pass(self, password):
        return bcrypt.hashpw(password,bcrypt.gensalt())

    def check_create(self, data):
        errors = []
        if len(data['name']) < 3:
            errors.append(['name', "Name must be at least 3 characters in length"])
        if len(data['username']) < 3:
            errors.append(['username', "Username must be at least 3 characters in length"])
        if len(data['password']) < 8:
            errors.append(['password',"Password must be at least eight characters"])
        if not data['password'] == data['confirmpass']:
            errors.append(['confirmpass', 'Passwords do not match'])
        if errors:
            return [False, errors]
        else:
            current_user = UserDB.objects.filter(username=data['username'])
            for user in current_user:
                print user
            if current_user:
                errors.append(['current_user',"User already exist, please use alternative information"])
                return [False, errors]
            else:
                newUser = UserDB(name=data['name'],username=data['username'], hashpw=self.hash_pass(data['password'].encode()))
                newUser.save()
                return [True, newUser]
    def check_log(self, data):
        errors = []
        current_user = UserDB.objects.filter(username=data['username'])
        print current_user
        if not current_user:
            errors.append(['account',"username incorrect"])
        elif not bcrypt.checkpw(data['password'].encode(),current_user[0].hashpw.encode()):
            errors.append(['account', "password incorrect"])
        if errors:
            return [False, errors]
        else:
            return [True, current_user[0]]

class TravelDBManager(models.Manager):
    def add(self, data, userid):
        errors = []
        if len(data['destination']) < 1:
            errors.append(['destination', "Destination cannot be empty."])
        if len(data['description']) < 1:
            errors.append(['description', "Description cannot be empty."])
        if not data['startdate']:
            errors.append(['startdate', "Start date cannot be empty."])
        if not data['enddate']:
            errors.append(['enddate', "End date cannot be empty."])
        if data['startdate'] < str(datetime.date.today()):
            errors.append(['startdate', "Start date only allows current and future dates."])
        if data['startdate'] > data['enddate']:
            errors.append(['enddate', "End date needs to be later than start date."])
        if errors:
            return [False, errors]
        else:
            user = UserDB.objects.get(id=userid)
            newTravel = TravelDB(planuser=user, destination = data['destination'], description = data['description'], startdate = data['startdate'], enddate = data['enddate'], )
            newTravel.save()
        return [True, newTravel]

    def join(self,id,userid):
        travel=TravelDB.objects.get(id=id)
        user=UserDB.objects.get(id=userid)
        travel.joinusers.add(user)
        travel.save()
        return True


class UserDB(models.Model):
    name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False)
    hashpw = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserDBManager()


class TravelDB(models.Model):
    planuser = models.ForeignKey(UserDB)
    joinusers = models.ManyToManyField(UserDB,related_name='travels')
    destination = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    startdate = models.DateField()
    enddate = models.DateField()
    objects = TravelDBManager()
