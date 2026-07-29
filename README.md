# Mech-Buddies — Online Roadside Assistance Platform

![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-4.1-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A Django web app connecting drivers with roadside assistance services — fuel delivery, towing, tire/wheel repair, and more — with online booking and a payment flow.

**Live Demo Link:** https://mechbuddies.pythonanywhere.com

**GitHub Repository** https://github.com/IN-Phantom-AKR/Mech-Buddies

## Tech Stack

- **Backend:** Django 4.1 (Python)
- **Database:** SQLite (dev)
- **Frontend:** Django templates + Bootstrap 5
- **Payments:** Mock payment gateway by default; real Paytm checksum-based integration available (toggle in settings)

## Features

- Customer sign-up/login (session-based, hashed passwords)
- Service catalog (DB-driven, seeded via management command)
- Vehicle garage — save vehicles to speed up future bookings
- Checkout with simulated payment (approve/decline), switchable to real Paytm
- Service request tracking (Pending → In Progress → Completed/Cancelled)
- Customer support contact form
- Dark/light mode toggle

---

## Project Structure
Mech-Buddies/
├── manage.py
├── Roadside_Assistance/ # project settings, root urls
├── Home/ # main app: models, views, urls, forms
│ └── management/commands/seed_services.py
├── Paytm/
│ └── Checksum.py # payment checksum generation/verification
├── templates/ # HTML templates
├── static/ # CSS, JS, images
└── Documentation/
└── Mech-Buddies_Docs.pdf # requirements, DFDs, use case diagram, data dictionary

---

## Setup & Run

```bash
git clone https://github.com/IN-Phantom-AKR/Mech-Buddies.git
cd Mech-Buddies

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install django pycryptodome

python manage.py migrate
python manage.py seed_services
python manage.py createsuperuser   # optional
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Admin panel: `http://127.0.0.1:8000/admin/`.

## Payment Modes

Set in `Roadside_Assistance/settings.py`:

```python
PAYMENT_MODE = 'mock'    # simulated payment, no external calls (default)
PAYMENT_MODE = 'paytm'   # real Paytm gateway — requires valid MERCHANT_KEY and MID in Home/views.py
```

## Known Limitations

- Paytm `MERCHANT_KEY`/`MID` in `views.py` are placeholders.
- Checkout requires login.
- No Service Provider portal yet.

## Documentation

Full requirements, DFDs, use case diagram, and data dictionary: `Documentation/Mech-Buddies_Docs.pdf`.

## Contributors

- Tanmay Chowdhary
- Ashish Sah
- Ashish
- Tanisha Kriplani

**Supervisor:** Mr. Suyash Kumar

## License

MIT — see [LICENSE](LICENSE)
