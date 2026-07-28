import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from Home.models import (
    SignUp, Customer_Support, Orders, OrderUpdate,
    Vehicle, Service, ServiceRequest, Payment,
)
from Home.forms import VehicleForm
from Home.decorators import login_required_custom
from Paytm import Checksum

MERCHANT_KEY = 'TestKey123456789'  # 16 chars — replace with your real Paytm merchant key when going live


def index(request):
    return render(request, 'Home.html')


def About(request):
    return render(request, 'About.html')


def FAQ(request):
    return render(request, 'FAQ.html')


def Login(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'After_Login'

    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        try:
            user = SignUp.objects.get(Email=email)
        except SignUp.DoesNotExist:
            return render(request, 'Login.html', {'error': 'Invalid email or password', 'next': next_url})

        if check_password(password, user.Password):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.Name
            return redirect(next_url)

        return render(request, 'Login.html', {'error': 'Invalid email or password', 'next': next_url})

    return render(request, 'Login.html', {'next': next_url})


def Logout(request):
    request.session.flush()
    return redirect('Home')


def Sign_up(request):
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        Address = request.POST.get('Address')
        City = request.POST.get('City')
        State = request.POST.get('State')
        Zip = request.POST.get('Zip')

        if SignUp.objects.filter(Email=Email).exists():
            return render(request, 'Sign_up.html', {'error': 'An account with this email already exists'})

        sign_up = SignUp(
            Name=Name, Email=Email, Password=make_password(Password),
            Address=Address, City=City, State=State, Zip=Zip
        )
        sign_up.save()

        request.session['user_id'] = sign_up.id
        request.session['user_name'] = sign_up.Name
        return redirect('After_Login')

    return render(request, 'Sign_up.html')


def Forget_password(request):
    return render(request, 'Forget_password.html')


def Services(request):
    services = Service.objects.all()
    return render(request, 'Services.html', {'services': services})


@login_required_custom
def Vehicles(request):
    customer = request.current_user

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer = customer
            vehicle.vehicle_id = f"{(vehicle.brand or 'VEH')[:3].upper()}{uuid.uuid4().hex[:6].upper()}"
            vehicle.save()
            return redirect('Vehicles')
    else:
        form = VehicleForm()

    my_vehicles = Vehicle.objects.filter(customer=customer)
    return render(request, 'Vehicles.html', {'form': form, 'vehicles': my_vehicles})


@login_required_custom
def My_Requests(request):
    customer = request.current_user
    requests_qs = ServiceRequest.objects.filter(customer=customer).order_by('-requested_at')
    return render(request, 'My_Requests.html', {'requests': requests_qs})


@login_required_custom
def Checkout(request):
    customer = request.current_user
    service_id = request.GET.get('service_id') or request.POST.get('service_id')
    selected_service = Service.objects.filter(service_id=service_id).first() if service_id else None
    my_vehicles = Vehicle.objects.filter(customer=customer)

    if request.method == "POST":
        if not selected_service:
            return render(request, 'Checkout.html', {
                'error': 'Please select a service from the Services page before checking out.',
                'vehicles': my_vehicles,
            })

        # Server decides the amount — the form never sends a trusted amount.
        amount = selected_service.price

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        vehicle_id = request.POST.get('vehicle_id')

        order = Orders(
            items_json=selected_service.service_name, name=name, email=email, address=address,
            city=city, state=state, zip_code=zip_code, phone=phone, amount=int(amount)
        )
        order.save()

        OrderUpdate.objects.create(order_id=order.order_id, update_desc="The order has been placed")

        chosen_vehicle = Vehicle.objects.filter(vehicle_id=vehicle_id, customer=customer).first() if vehicle_id else None
        service_request = ServiceRequest.objects.create(
            request_id=f"REQ{order.order_id}{uuid.uuid4().hex[:4].upper()}",
            customer=customer,
            vehicle=chosen_vehicle,
            service=selected_service,
            location=f"{address}, {city}, {state} {zip_code}",
            status='PENDING',
        )

        request.session['pending_request_id'] = service_request.request_id
        request.session['pending_order_id'] = order.order_id
        request.session['pending_amount'] = str(amount)

        if getattr(settings, 'PAYMENT_MODE', 'mock') == 'mock':
            return redirect('MockPayment')

        # --- Real Paytm flow (kept ready for when you have real merchant credentials) ---
        param_dict = {
            'MID': 'Merchantid_2484',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'Paytm.html', {'param_dict': param_dict})

    return render(request, 'Checkout.html', {
        'selected_service': selected_service,
        'vehicles': my_vehicles,
    })


def mock_payment(request):
    """Simulated payment screen — used when settings.PAYMENT_MODE == 'mock'."""
    order_id = request.session.get('pending_order_id')
    amount = request.session.get('pending_amount')
    if not order_id:
        return redirect('Home')

    order = Orders.objects.filter(order_id=order_id).first()
    return render(request, 'MockPayment.html', {'order': order, 'amount': amount})


def mock_payment_process(request):
    """Handles the simulated Approve/Decline click and writes the same
    Payment/OrderUpdate/ServiceRequest records a real gateway callback would."""
    if request.method != 'POST':
        return redirect('Home')

    outcome = request.POST.get('outcome')  # 'success' or 'failure'
    order_id = request.session.get('pending_order_id')
    request_id = request.session.get('pending_request_id')
    order = Orders.objects.filter(order_id=order_id).first()

    response_dict = {
        'ORDERID': str(order_id) if order_id else '',
        'TXN_AMOUNT': str(order.amount) if order else '',
        'PAYMENTMODE': 'MOCK',
    }

    if outcome == 'success':
        response_dict['RESPCODE'] = '01'
        response_dict['RESPMSG'] = 'Txn Success (Simulated)'

        if order_id:
            OrderUpdate.objects.create(order_id=order_id, update_desc="Payment successful (mock)")

        if request_id:
            service_request_obj = ServiceRequest.objects.filter(request_id=request_id).first()
            if service_request_obj:
                service_request_obj.status = 'IN_PROGRESS'
                service_request_obj.save()
                if order:
                    Payment.objects.create(
                        payment_id=f"PAY{order_id}{uuid.uuid4().hex[:4].upper()}",
                        service_request=service_request_obj,
                        customer=service_request_obj.customer,
                        amount=order.amount,
                        payment_method='MOCK',
                    )
    else:
        response_dict['RESPCODE'] = '400'
        response_dict['RESPMSG'] = 'Txn Failed (Simulated)'

        if order_id:
            OrderUpdate.objects.create(order_id=order_id, update_desc="Payment failed (mock — declined)")
        if request_id:
            ServiceRequest.objects.filter(request_id=request_id).update(status='CANCELLED')

    request.session.pop('pending_order_id', None)
    request.session.pop('pending_request_id', None)
    request.session.pop('pending_amount', None)

    return render(request, 'Paymentstatus.html', {'response': response_dict})


@csrf_exempt
def handlerequest(request):
    """Real Paytm callback handler — only reached when PAYMENT_MODE == 'paytm'."""
    if request.method != 'POST':
        return HttpResponse(
            f"Expected a POST from Paytm, got {request.method}. "
            f"You may have navigated here directly rather than being redirected by Paytm.",
            status=400
        )

    form = request.POST
    response_dict = {}
    checksum = None

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    if checksum is None:
        return render(request, 'Paymentstatus.html', {
            'response': response_dict,
            'error': 'No checksum received from Paytm — likely means MID is not a registered merchant account.'
        })

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if not verify:
        return render(request, 'Paymentstatus.html', {
            'response': response_dict,
            'error': 'Checksum verification failed.'
        })

    order_id = response_dict.get('ORDERID')
    request_id = request.session.get('pending_request_id')

    if response_dict.get('RESPCODE') == '01':
        if order_id:
            OrderUpdate.objects.create(order_id=order_id, update_desc="Payment successful")
        if request_id:
            service_request_obj = ServiceRequest.objects.filter(request_id=request_id).first()
            if service_request_obj:
                service_request_obj.status = 'IN_PROGRESS'
                service_request_obj.save()
                order = Orders.objects.filter(order_id=order_id).first()
                if order:
                    Payment.objects.create(
                        payment_id=f"PAY{order_id}{uuid.uuid4().hex[:4].upper()}",
                        service_request=service_request_obj,
                        customer=service_request_obj.customer,
                        amount=order.amount,
                        payment_method=response_dict.get('PAYMENTMODE', 'Paytm'),
                    )
    else:
        if order_id:
            OrderUpdate.objects.create(
                order_id=order_id,
                update_desc=f"Payment failed: {response_dict.get('RESPMSG', 'unknown error')}"
            )
        if request_id:
            ServiceRequest.objects.filter(request_id=request_id).update(status='CANCELLED')

    return render(request, 'Paymentstatus.html', {'response': response_dict})


def Customer(request):
    if request.method == 'POST':
        Email = request.POST.get('Email')
        Comment = request.POST.get('Comment')
        Customer_Support.objects.create(Email=Email, Comment=Comment)
        return render(request, 'Customer.html', {'success': True})
    return render(request, 'Customer.html')


def After_Login(request):
    return render(request, 'After_Login.html')