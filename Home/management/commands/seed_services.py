from django.core.management.base import BaseCommand
from Home.models import Service

SERVICES = [
    ("SVC001", "Fuel Delivery", "Run out of fuel? We provide fast, reliable emergency fuel delivery.", 500.00, "fuel.png"),
    ("SVC002", "Engine Diagnostic", "Check engine light on? We diagnose and repair engine issues quickly.", 800.00, "engine.png"),
    ("SVC003", "Wheel Alignment", "Car pulling to one side? We realign your wheels in no time.", 600.00, "wheel.png"),
    ("SVC004", "Mechanical Fault", "General mechanical repairs and maintenance to get you back on the road.", 900.00, "mech.png"),
    ("SVC005", "AC Repair", "Car AC not cooling? Our experts get it running again.", 700.00, "ac.png"),
    ("SVC006", "Oil Change", "Quick, hassle-free oil change service.", 400.00, "oil.png"),
    ("SVC007", "Key Lockout", "Locked out of your car? We help you get back in.", 350.00, "key.png"),
    ("SVC008", "Brake Repair", "Faulty brakes fixed for your safety.", 850.00, "breakrepair.png"),
    ("SVC009", "Car Wash", "Top-notch automobile washing service.", 250.00, "carwash.png"),
    ("SVC010", "Car Paint", "Touch-up paint to full paint jobs.", 3000.00, "paint.png"),
    ("SVC011", "Automobile Designing", "Custom repairs and maintenance for any issue.", 1200.00, "design.png"),
    ("SVC012", "Vehicle Tow", "Reliable towing for breakdowns and accidents.", 1000.00, "vehicletow.png"),
]


class Command(BaseCommand):
    help = "Seeds the Service table with the default Mech-Buddies service catalog"

    def handle(self, *args, **options):
        created_count = 0
        for service_id, name, desc, price, image in SERVICES:
            _, created = Service.objects.get_or_create(
                service_id=service_id,
                defaults={'service_name': name, 'description': desc, 'price': price, 'image_name': image}
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} new services."))