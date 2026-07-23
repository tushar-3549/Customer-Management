from django.contrib import admin

from .models import (
    Customer,
    MobileNumber,
    Address,
    Document,
)


class MobileNumberInline(admin.TabularInline):
    model = MobileNumber
    extra = 1


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "national_id",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "national_id",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        MobileNumberInline,
        AddressInline,
        DocumentInline,
    ]


@admin.register(MobileNumber)
class MobileNumberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "number",
        "mobile_type",
    )

    search_fields = (
        "number",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "address_type",
        "city",
        "district",
    )

    list_filter = (
        "address_type",
        "city",
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "document_type",
        "uploaded_at",
    )

    list_filter = (
        "document_type",
    )