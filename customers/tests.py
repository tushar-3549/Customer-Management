from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer


class CustomerAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("customer-list-create")

        self.payload = {
            "name": "Md Tushar Ahmed",
            "email": "tushar@example.com",
            "date_of_birth": "2001-08-15",
            "national_id": "1234567890123",
            "status": "ACTIVE",
            "mobile_numbers": [
                {
                    "number": "01711111111",
                    "mobile_type": "PRIMARY"
                }
            ],
            "addresses": [
                {
                    "address_type": "PRESENT",
                    "address": "Dhanmondi",
                    "city": "Dhaka",
                    "district": "Dhaka",
                    "postal_code": "1209",
                    "country": "Bangladesh"
                }
            ],
            "documents": []
        }

    def test_create_customer(self):
        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Customer.objects.count(),
            1,
        )

    def test_get_customer_list(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_get_customer_by_id(self):
        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        customer_id = response.data["id"]

        detail_url = reverse(
            "customer-detail",
            kwargs={"pk": customer_id},
        )

        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_customer(self):
        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        customer_id = response.data["id"]

        detail_url = reverse(
            "customer-detail",
            kwargs={"pk": customer_id},
        )

        payload = self.payload.copy()
        payload["name"] = "Updated Name"

        response = self.client.put(
            detail_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_customer(self):
        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        customer_id = response.data["id"]

        detail_url = reverse(
            "customer-detail",
            kwargs={"pk": customer_id},
        )

        response = self.client.delete(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_future_date_of_birth(self):
        payload = self.payload.copy()
        payload["date_of_birth"] = "2099-01-01"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_email(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_duplicate_mobile(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        payload = self.payload.copy()
        payload["email"] = "another@example.com"
        payload["national_id"] = "999999999999"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_duplicate_national_id(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        payload = self.payload.copy()
        payload["email"] = "new@example.com"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_customer_not_found(self):
        detail_url = reverse(
            "customer-detail",
            kwargs={"pk": 9999},
        )

        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_search_customer(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        response = self.client.get(
            self.url + "?search=Tushar"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_filter_customer(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        response = self.client.get(
            self.url + "?status=ACTIVE"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_sort_customer(self):
        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        response = self.client.get(
            self.url + "?ordering=name"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_pagination(self):
        for i in range(15):
            payload = {
                "name": f"Customer {i}",
                "email": f"customer{i}@mail.com",
                "date_of_birth": "2000-01-01",
                "national_id": f"123456789{i}",
                "status": "ACTIVE",
                "mobile_numbers": [
                    {
                        "number": f"01700000{i:03}",
                        "mobile_type": "PRIMARY",
                    }
                ],
                "addresses": [
                    {
                        "address_type": "PRESENT",
                        "address": "Dhaka",
                        "city": "Dhaka",
                        "district": "Dhaka",
                        "postal_code": "1207",
                        "country": "Bangladesh",
                    }
                ],
                "documents": [],
            }

            self.client.post(
                self.url,
                payload,
                format="json",
            )

        response = self.client.get(
            self.url + "?page=1&page_size=5"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_patch_customer(self):
        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        customer_id = response.data["id"]

        detail_url = reverse(
            "customer-detail",
            kwargs={"pk": customer_id},
        )

        response = self.client.patch(
            detail_url,
            {
                "name": "Patched Customer"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_delete_not_found(self):
        detail_url = reverse(
            "customer-detail",
            kwargs={"pk": 1000},
        )

        response = self.client.delete(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )