from django.contrib import admin
from Home.models import (
    SignUp, Customer_Support, Orders, OrderUpdate,
    Vehicle, Service, ServiceProvider, ServiceRequest, Payment,
)

admin.site.register(SignUp)
admin.site.register(Customer_Support)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Vehicle)
admin.site.register(Service)
admin.site.register(ServiceProvider)
admin.site.register(ServiceRequest)
admin.site.register(Payment)