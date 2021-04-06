from django.db import models


class Order(models.Model):
    """ Order Class

        - id: Unique id for the order
        - customer_name: First Name
        - customer_surname: Last Name
        - customer_doctype: Document Type
        - customer_document: Number of document
        - customer_email: Email
        - customer_mobile: Phone
        - status: Order status
        - created_at: Date of order creation
        - updated_at: Date of order update
    """
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=80)
    customer_surname = models.CharField(max_length=80)
    customer_doc_type = models.CharField(max_length=30, default="CC")
    customer_document = models.CharField(max_length=32)
    customer_email = models.CharField(max_length=120)
    customer_mobile = models.CharField(max_length=40)
    status = models.CharField(max_length=20, default="CREATED")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    request_id = models.CharField(max_length=60, default="")
    process_url = models.CharField(max_length=250, default="")
