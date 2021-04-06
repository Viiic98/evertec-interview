from django import forms


class RawOrderForm(forms.Form):
    """ Order Form Creation """
    customer_name = forms.CharField(max_length=80, label='Name')
    customer_surname = forms.CharField(max_length=80, label='Surname')
    customer_doc_type = forms.CharField(max_length=80, label='Document Type')
    customer_document = forms.CharField(max_length=80, label='Document')
    customer_email = forms.CharField(max_length=120, label='Email')
    customer_mobile = forms.CharField(max_length=40, label='Phone')


class RequestId(forms.Form):
    """ Form used to check order status """
    request_id = forms.CharField(label='Request Id', max_length=50)
