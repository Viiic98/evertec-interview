from django.shortcuts import render, redirect
from .forms import RawOrderForm, RequestId
from .models import Order
from .auth import RedirectionAuth
import requests
from datetime import datetime, timedelta


# URL to the placetopay test API
URL = 'https://test.placetopay.com/redirection/api/session'
# Initialize data for the session
data = {
    "paymentMethod": None,
    "payment": {
        "reference": "TEST_20210405_175107",
        "description": "RAM DDR4 16GB",
        "amount": {
            "currency": "COP",
            "total": 144000
        }
    },
    "expiration": (datetime.now() + timedelta(days=1)).isoformat(),
    "returnUrl": "http://127.0.0.1:8000/status",
    "ipAddress": "127.0.0.1",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                 "AppleWebKit/537.36 (KHTML, like Gecko)"
                 "Chrome/89.0.4389.114 Safari/537.36",
}


def transaction(request):
    """ Create transaction """
    form = RawOrderForm()
    context = {
        'form': form
    }
    # Initialize order
    data['order'] = ''
    if request.method == 'POST':
        form = RawOrderForm(request.POST)
        if form.is_valid():
            new_transaction = form.cleaned_data
            # Customer Information
            data['buyer'] = {
                'name': new_transaction['customer_name'],
                'surname': new_transaction['customer_surname'],
                'email': new_transaction['customer_email'],
                'mobile': new_transaction['customer_mobile'],
                "documentType": new_transaction['customer_doc_type'],
                "document": new_transaction['customer_document'],
            }
            new_transaction['status'] = 'CREATED'
            # Authentication
            auth = RedirectionAuth().get_auth()
            data['auth'] = auth
            print(data)
            r = requests.post(URL, json=data)
            response = r.json()
            # Store request id and process url
            data['request_id'] = response['requestId']
            data['process_url'] = response['processUrl']
            new_transaction['request_id'] = response['requestId']
            new_transaction['process_url'] = response['processUrl']
            # Create the new order in database
            data['order'] = Order.objects.create(**new_transaction)
            return redirect('created')
        else:
            print(form.errors)
    return render(request, "transaction.html", context)


def created(request):
    """ Display order created """
    context = {
        'request_id': data['request_id'],
        'process_url': data['process_url'],
        'desc': data['payment']['description'],
        'amount': data['payment']['amount'],
        'buyer': data['buyer']
    }
    return render(request, "created.html", context)


def status(request):
    """ Display order status

        POST: Check the status of an order
        GET: Redirection from placetopay, display status
             after get back from the process URL
    """
    if request.method == 'POST':
        form = RequestId(request.POST)
        if form.is_valid():
            data['request_id'] = form.cleaned_data['request_id']
            auth = RedirectionAuth().get_auth()
            data['auth'] = auth
    r = requests.post(URL + '/' + str(data['request_id']),
                      json={'auth': data['auth']})
    response = r.json()

    context = {
        'request_id': data['request_id'],
        'current_status': response['status'],
        'buyer': response['request']['buyer']
    }
    if response['status']['status'] == 'PENDING':
        context['process_url'] = data['process_url']
    if request.method == 'GET':
        data['order'].status = response['status']['status']
        data['order'].save()
        context['process_url'] = data['process_url']
    return render(request, "status.html", context)


def check(request):
    """ Form to check order status """
    form = RequestId()
    context = {
        'form': form
    }
    return render(request, "check.html", context)


def orders(request):
    """ Display all the orders created """
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, "orders.html", context)
