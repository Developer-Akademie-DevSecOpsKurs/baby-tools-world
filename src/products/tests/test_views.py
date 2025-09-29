from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import Product


User = get_user_model()


class ProductViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="tester", email="t@example.com", password="pass1234"
        )
        cls.other_user = User.objects.create_user(
            username="other", email="o@example.com", password="pass1234"
        )
        cls.product = Product.objects.create(
            name="Blue Rattle",
            slug="blue-rattle",
            description="Test product",
            price=9.99,
        )

    # --------- List View ---------
    def test_product_list_ok(self):
        url = reverse("products:list")  # e.g. path("products/", ..., name="list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.product, resp.context["object_list"])

    # --------- Detail View ---------
    def test_product_detail_ok(self):
        url = reverse("products:detail", args=[self.product.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["object"], self.product)

    def test_product_detail_404(self):
        url = reverse("products:detail", args=["does-not-exist"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    # --------- Create View ---------
    def test_product_create_requires_login(self):
        url = reverse("products:create")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (302, 401, 403))

    def test_product_create_invalid(self):
        self.client.login(username="tester", password="pass1234")
        url = reverse("products:create")
        resp = self.client.post(url, data={
            "name": "",             # invalid: required
            "description": "x",
            "price": ""             # invalid: required/format
        })
        self.assertEqual(resp.status_code, 200)  # form re-render
        self.assertFormError(resp, "form", "name", "This field is required.")

    def test_product_create_ok(self):
        self.client.login(username="tester", password="pass1234")
        url = reverse("products:create")
        resp = self.client.post(url, data={
            "name": "Teether",
            "description": "Nice",
            "price": "4.50",
        })
        self.assertIn(resp.status_code, (302, 303))
        self.assertTrue(Product.objects.filter(name="Teether").exists())

    # --------- Update View ---------
    def test_product_update_forbidden_if_not_owner(self):
        # Adjust if ownership logic differs
        self.client.login(username="other", password="pass1234")
        url = reverse("products:update", args=[self.product.slug])
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (403, 404))

    def test_product_update_ok(self):
        # If ownership needed, ensure self.product.user = self.user in setUpTestData
        self.client.login(username="tester", password="pass1234")
        url = reverse("products:update", args=[self.product.slug])
        resp = self.client.post(url, data={
            "name": "Blue Rattle Updated",
            "description": "Test product",
            "price": "10.50",
        })
        self.assertIn(resp.status_code, (302, 303))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Blue Rattle Updated")

    # --------- Delete View ---------
    def test_product_delete_requires_login(self):
        url = reverse("products:delete", args=[self.product.slug])
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 401, 403))

    def test_product_delete_ok(self):
        self.client.login(username="tester", password="pass1234")
        url = reverse("products:delete", args=[self.product.slug])
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 303))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    # --------- Search / Filter (if applicable) ---------
    def test_product_list_search(self):
        url = reverse("products:list")
        resp = self.client.get(url, {"q": "Blue"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.product, resp.context["object_list"])

    # --------- API JSON endpoint example (optional) ---------
    def test_product_detail_json(self):
        # Only if you have a JSON route, adjust name/path
        url = reverse("products:detail-json", args=[self.product.slug])
        resp = self.client.get(url, HTTP_ACCEPT="application/json")
        if resp.status_code == 200:
            data = resp.json()
            self.assertEqual(data["name"], self.product.name)
        else:
            # Skip if endpoint not implemented
            self.assertIn(resp.status_code, (404,))
