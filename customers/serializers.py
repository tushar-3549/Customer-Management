from datetime import date

from rest_framework import serializers

from .models import Customer, MobileNumber, Address, Document


class MobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileNumber
        fields = ["id", "number", "mobile_type"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address_type",
            "address",
            "city",
            "district",
            "postal_code",
            "country",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "document_type",
            "file",
            "uploaded_at",
        ]
        read_only_fields = ["uploaded_at"]


class CustomerSerializer(serializers.ModelSerializer):
    mobile_numbers = MobileNumberSerializer(many=True)
    addresses = AddressSerializer(many=True)
    documents = DocumentSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "date_of_birth",
            "national_id",
            "status",
            "created_at",
            "updated_at",
            "mobile_numbers",
            "addresses",
            "documents",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Customer name is required.")
        return value

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be a future date."
            )
        return value

    def create(self, validated_data):
        mobiles = validated_data.pop("mobile_numbers", [])
        addresses = validated_data.pop("addresses", [])
        documents = validated_data.pop("documents", [])

        customer = Customer.objects.create(**validated_data)

        for mobile in mobiles:
            MobileNumber.objects.create(customer=customer, **mobile)

        for address in addresses:
            Address.objects.create(customer=customer, **address)

        for document in documents:
            Document.objects.create(customer=customer, **document)

        return customer

    def update(self, instance, validated_data):
        mobiles = validated_data.pop("mobile_numbers", None)
        addresses = validated_data.pop("addresses", None)
        documents = validated_data.pop("documents", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if mobiles is not None:
            instance.mobile_numbers.all().delete()
            for mobile in mobiles:
                MobileNumber.objects.create(
                    customer=instance,
                    **mobile,
                )

        if addresses is not None:
            instance.addresses.all().delete()
            for address in addresses:
                Address.objects.create(
                    customer=instance,
                    **address,
                )

        if documents is not None:
            instance.documents.all().delete()
            for document in documents:
                Document.objects.create(
                    customer=instance,
                    **document,
                )

        return instance