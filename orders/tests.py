from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

class UserOrdersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_user_orders(self):
        user_id = 1
        response = self.client.get(f"/user/{user_id}/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrdersViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_all_orders(self):
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AddToCartAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_to_cart(self):
        user_id = 1
        product_id = 1
        data = {"Quantity": 1}
        response = self.client.post(f"/user/{user_id}/cart/{product_id}/add/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CartCheckAVTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_cart_items(self):
        user_id = 1
        response = self.client.get(f"/user/{user_id}/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CartCheckViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_check_cart(self):
        user_id = 1
        response = self.client.get(f"/user/{user_id}/cart/check/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CheckoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_checkout(self):
        user_id = 1
        response = self.client.post(f"/user/{user_id}/checkout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ItemDetailsAVTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_item_details(self):
        user_id = 1
        item_id = 1
        response = self.client.get(f"/item/{item_id}/details/{user_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item_quantity(self):
        user_id = 1
        item_id = 1
        data = {"Quantity": 2}
        response = self.client.patch(f"/item/{item_id}/details/{user_id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        user_id = 1
        item_id = 1
        response = self.client.delete(f"/item/{item_id}/details/{user_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CreatePaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_payment(self):
        response = self.client.post("/payment/create/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PaymentStatusTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_payment_status(self):
        invoice_number = "ABC123"
        response = self.client.get(f"/payment/{invoice_number}/status/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ConfirmPaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_confirm_payment(self):
        response = self.client.post("/payment/confirm/")
        self.assertEqual(response.status)
