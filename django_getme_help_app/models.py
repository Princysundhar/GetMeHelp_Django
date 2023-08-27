from django.db import models

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

class User(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    house_name = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    email = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    LOGIN = models.ForeignKey(Login,on_delete=models.CASCADE,default=1)

class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    account_no = models.BigIntegerField()
    IFSC_code = models.CharField(max_length=100)
    amount = models.IntegerField()
    LOGIN = models.ForeignKey(Login,on_delete=models.CASCADE,default=1)

class Category(models.Model):
    category = models.CharField(max_length=100)

class Worker(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    photo = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    lattitude = models.CharField(max_length=100,default=1)
    longitude = models.CharField(max_length=100,default=1)
    CATEGORY = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE, default=1)

class Service(models.Model):
    service = models.CharField(max_length=100)
    amount = models.IntegerField()
    WORKER = models.ForeignKey(Worker,on_delete=models.CASCADE,default=1)

class Bookings(models.Model):
    date = models.CharField(max_length=100)
    amount = models.IntegerField()
    lattitude = models.CharField(max_length=100, default=1)
    longitude = models.CharField(max_length=100, default=1)
    status = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100,default=1)
    USER = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    SERVICE = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)

class Bill(models.Model):
    amount = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    BOOKING = models.ForeignKey(Bookings,on_delete=models.CASCADE,default=1)

class Rating(models.Model):
    rate = models.IntegerField()
    date = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    # SERVICE = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)
    # USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    BOOKINGS=models.ForeignKey(Bookings,on_delete=models.CASCADE,default=1)

# class Payment(models.Model):
#     amount = models.IntegerField()
#     date = models.CharField(max_length=100)
#     USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     BILL = models.ForeignKey(Bill,on_delete=models.CASCADE,default=1)

class Credit_point(models.Model):
    credit_point = models.CharField(max_length=100)
    # USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE, default=1)

class Chat(models.Model):
    date = models.CharField(max_length=100)
    chat = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    WORKER = models.ForeignKey(Worker, on_delete=models.CASCADE, default=1)

class Complaint(models.Model):
    complaint = models.CharField(max_length=100)
    complaint_date = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    reply_date = models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)