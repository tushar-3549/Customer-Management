from .models import Customer


class CustomerRepository:

    @staticmethod
    def create(data):
        return Customer.objects.create(**data)

    @staticmethod
    def get_all():
        return Customer.objects.prefetch_related(
            "mobile_numbers",
            "addresses",
            "documents",
        ).all()

    @staticmethod
    def get_by_id(customer_id):
        return Customer.objects.prefetch_related(
            "mobile_numbers",
            "addresses",
            "documents",
        ).filter(id=customer_id).first()

    @staticmethod
    def update(customer):
        customer.save()
        return customer

    @staticmethod
    def delete(customer):
        customer.delete()

    @staticmethod
    def exists_email(email):
        return Customer.objects.filter(email=email).exists()

    @staticmethod
    def exists_nid(national_id):
        return Customer.objects.filter(
            national_id=national_id
        ).exists()