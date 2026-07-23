from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import CustomerSerializer
from .services import CustomerService


class CustomerListCreateAPIView(APIView):

    def get(self, request):
        queryset = CustomerService.get_customers()

        search = request.GET.get("search")
        status_filter = request.GET.get("status")
        ordering = request.GET.get("ordering")

        if search:
            queryset = queryset.filter(name__icontains=search)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = CustomerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = CustomerService.create_customer(serializer)

        return Response(
            CustomerSerializer(customer).data,
            status=status.HTTP_201_CREATED,
        )

    # Pagination Helpers
    from rest_framework.pagination import PageNumberPagination

    pagination_class = PageNumberPagination

    def paginate_queryset(self, queryset):
        paginator = self.pagination_class()
        paginator.page_size = int(
            self.request.GET.get("page_size", 10)
        )
        self._paginator = paginator
        return paginator.paginate_queryset(
            queryset,
            self.request,
            view=self,
        )

    def get_paginated_response(self, data):
        return self._paginator.get_paginated_response(data)


class CustomerRetrieveUpdateDeleteAPIView(APIView):

    def get(self, request, pk):
        customer = CustomerService.get_customer(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = CustomerService.get_customer(pk)

        serializer = CustomerSerializer(
            customer,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        customer = CustomerService.update_customer(
            pk,
            serializer,
        )

        return Response(CustomerSerializer(customer).data)

    def patch(self, request, pk):
        customer = CustomerService.get_customer(pk)

        serializer = CustomerSerializer(
            customer,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        customer = CustomerService.update_customer(
            pk,
            serializer,
        )

        return Response(CustomerSerializer(customer).data)

    def delete(self, request, pk):
        CustomerService.delete_customer(pk)

        return Response(
            {
                "message": "Customer deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )