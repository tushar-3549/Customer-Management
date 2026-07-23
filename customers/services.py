from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound

from .models import Customer, MobileNumber, Address, Document
from .repositories import CustomerRepository


class CustomerService:

    @staticmethod
    @transaction.atomic
    def create_customer(serializer):
        email = serializer.validated_data["email"]
        national_id = serializer.validated_data["national_id"]

        if CustomerRepository.exists_email(email):
            raise ValidationError(
                {"email": "Email already exists."}
            )

        if CustomerRepository.exists_nid(national_id):
            raise ValidationError(
                {"national_id": "National ID already exists."}
            )

        for mobile in serializer.validated_data.get(
            "mobile_numbers", []
        ):
            if MobileNumber.objects.filter(
                number=mobile["number"]
            ).exists():
                raise ValidationError(
                    {
                        "mobile_number":
                        f'{mobile["number"]} already exists.'
                    }
                )

        return serializer.save()

    @staticmethod
    def get_customer(customer_id):
        customer = CustomerRepository.get_by_id(customer_id)

        if not customer:
            raise NotFound("Customer not found.")

        return customer

    @staticmethod
    def get_customers():
        return CustomerRepository.get_all()

    @staticmethod
    @transaction.atomic
    def update_customer(customer_id, serializer):
        customer = CustomerRepository.get_by_id(customer_id)

        if not customer:
            raise NotFound("Customer not found.")

        email = serializer.validated_data.get("email")

        if (
            email
            and Customer.objects.exclude(id=customer.id)
            .filter(email=email)
            .exists()
        ):
            raise ValidationError(
                {"email": "Email already exists."}
            )

        national_id = serializer.validated_data.get(
            "national_id"
        )

        if (
            national_id
            and Customer.objects.exclude(id=customer.id)
            .filter(national_id=national_id)
            .exists()
        ):
            raise ValidationError(
                {
                    "national_id":
                    "National ID already exists."
                }
            )

        mobiles = serializer.validated_data.get(
            "mobile_numbers", []
        )

        for mobile in mobiles:
            if MobileNumber.objects.exclude(
                customer=customer
            ).filter(number=mobile["number"]).exists():
                raise ValidationError(
                    {
                        "mobile_number":
                        f'{mobile["number"]} already exists.'
                    }
                )

        return serializer.save()

    @staticmethod
    def delete_customer(customer_id):
        customer = CustomerRepository.get_by_id(customer_id)

        if not customer:
            raise NotFound("Customer not found.")

        CustomerRepository.delete(customer)
        return True