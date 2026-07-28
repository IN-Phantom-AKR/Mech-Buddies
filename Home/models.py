from django.db import models


class SignUp(models.Model):
    Name = models.CharField(max_length=200, blank=True, null=True)
    Email = models.EmailField(max_length=200, blank=True, null=True)
    Password = models.CharField(max_length=200, blank=True, null=True)
    Address = models.CharField(max_length=500, blank=True, null=True)
    City = models.CharField(max_length=200, blank=True, null=True)
    State = models.CharField(max_length=200, blank=True, null=True)
    Zip = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.Name


class Customer_Support(models.Model):
    Email = models.EmailField(max_length=200, blank=True, null=True)
    Comment = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.Email


class Vehicle(models.Model):
    """Matches PDF Data Dictionary - Vehicle Table"""
    vehicle_id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='vehicles')
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    license_plate = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_id} ({self.brand} {self.model})"


class Service(models.Model):
    """Matches PDF Data Dictionary - Services Table (+ image_name for the front-end)"""
    service_id = models.CharField(max_length=50, primary_key=True)
    service_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_name = models.CharField(max_length=100, blank=True, null=True,
                                   help_text="Filename in /static, e.g. fuel.png")

    def __str__(self):
        return self.service_name


class ServiceProvider(models.Model):
    """Matches PDF Data Dictionary - Service Provider Table"""
    provider_id = models.CharField(max_length=50, primary_key=True)
    company_name = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.company_name


class ServiceRequest(models.Model):
    """Matches PDF Data Dictionary - Service Request Table"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    request_id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='service_requests')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    requested_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(
        ServiceProvider, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_requests'
    )
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.request_id} - {self.status}"


class Payment(models.Model):
    """Matches PDF Data Dictionary - Payment Table"""
    payment_id = models.CharField(max_length=50, primary_key=True)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(SignUp, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.payment_id} - {self.amount}"


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."