from django.db import models

# class customer, coloums: User, Name, Email, Phone number

class Customer(models.Model):
    user = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()

# class product, coloums: Name, Price, Image    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    image = models.ImageField()
    product_id = models.CharField(max_length=200)

# class feature, coloums: Product_feature

class Feature(models.Model):
    Product_feature = models.CharField(max_length=200)

# class review, coloums: customer, product, content, date_time

class Review(models.Model):
    customer = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    date_time = models.DateTimeField()

# class order, coloums: Customer, Date_ordered, complete

class Order(models.Model):
    customer = models.CharField(max_length=200)
    date_ordered = models.DateField()
    complete = models.CharField(max_length=200)

# class order_item, coloums: product, order, quantity, date_added

class Order_item(models.Model):
    product = models.CharField(max_length=200)
    order = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    date_added =  models.DateField()

# class update_order, coloums: Order_id, description, date

class Update_order(models.Model):
    order_id = models.IntegerField()
    description = models.CharField(max_length=200)
    date = models.DateField()

# class checkout_details, coloums: customer, order, phone_number, total_amount, address, city, state, zipcode, payment, date_added

class Checkout_details(models.Model):
    customer = models.CharField(max_length=200)
    order = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    total_amount = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city =  models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    payment = models.CharField(max_length=200)
    date_added = models.DateField()

# class contact, coloums: Name, email, phone_number, description

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    description = models.CharField(max_length=200)