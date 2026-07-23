from django.db import models


class Customer(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MobileNumber(models.Model):
    TYPE_CHOICES = (
        ("PRIMARY", "Primary"),
        ("ALTERNATE", "Alternate"),
        ("OFFICE", "Office"),
    )

    customer = models.ForeignKey(
        Customer,
        related_name="mobile_numbers",
        on_delete=models.CASCADE,
    )
    number = models.CharField(max_length=20, unique=True)
    mobile_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="PRIMARY"
    )

    def __str__(self):
        return self.number


class Address(models.Model):
    TYPE_CHOICES = (
        ("PRESENT", "Present"),
        ("PERMANENT", "Permanent"),
        ("MAILING", "Mailing"),
    )

    customer = models.ForeignKey(
        Customer,
        related_name="addresses",
        on_delete=models.CASCADE,
    )
    address_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Bangladesh")

    def __str__(self):
        return f"{self.customer.name} - {self.address_type}"


class Document(models.Model):
    TYPE_CHOICES = (
        ("NID", "NID"),
        ("PHOTO", "Photo"),
        ("SIGNATURE", "Signature"),
        ("TAX", "Tax Certificate"),
    )

    customer = models.ForeignKey(
        Customer,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    document_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.document_type}"