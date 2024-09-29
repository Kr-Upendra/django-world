from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    CUSTOMER_USER = 'U'
    CUSTOMER_ADMIN = 'A'
    CUSTOMER_ROLES = [
        (CUSTOMER_USER, 'User'),
        (CUSTOMER_ADMIN, 'Admin')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    customer_role = models.CharField(max_length=1,choices=CUSTOMER_ROLES, default=CUSTOMER_USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Address(models.Model):
    street = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    zip_code = models.CharField(max_length=6,default='000000')
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)


class Order(models.Model):
    ORDER_STATUS_PENDING = 'P'
    ORDER_STATUS_SHIPPED = 'S'
    ORDER_STATUS_DELIVERED = 'D'
    ORDER_STATUS = [
        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_SHIPPED, 'Shipped'),
        (ORDER_STATUS_DELIVERED, 'Delivered')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_status = models.CharField(max_length=1,choices=ORDER_STATUS, default=ORDER_STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(max_digits=10,decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField() 