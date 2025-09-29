from django.contrib.auth import get_user_model
from django.test import TestCase

from btw_app.utils import log_execution
from products.models import Category, Comment, Product

User = get_user_model()


class CommentTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Base fixtures
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            name="Test Product",
            price="19.99",
            category=self.category,
        )
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="pass1234")
        self.content = "This is a test comment."
        # If your model has rating (e.g. PositiveSmallIntegerField 1-5), adapt/remove related tests.
        self.valid_rating = 5

    def setUp(self):
        Comment.objects.all().delete()

    # SUCCESS TESTS
    @log_execution
    def test_successful_comment_creation_minimal(self):
        comment = Comment.objects.create(
            product=self.product,
            user=self.user,
            content=self.content,
        )
        comment.full_clean()
        self.assertEqual(Comment.objects.count(), 1)
        stored = Comment.objects.first()
        self.assertEqual(stored.product, self.product)
        self.assertEqual(stored.user, self.user)
        self.assertEqual(stored.content, self.content)
        self.assertIsNotNone(stored.created_at)
        self.assertIsNotNone(stored.updated_at)

    @log_execution
    def test_successful_comment_creation_with_rating(self):
        # Remove or adapt if no rating field exists.
        comment = Comment.objects.create(
            product=self.product,
            user=self.user,
            content=self.content,
            rating=self.valid_rating,
        )
        comment.full_clean()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().rating, self.valid_rating)

    # FAILURE TESTS
    @log_execution
    def test_failure_comment_creation_without_user(self):
        with self.assertRaises(Exception):
            comment = Comment(
                product=self.product,
                content=self.content,
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_failure_comment_creation_without_product(self):
        with self.assertRaises(Exception):
            comment = Comment(
                user=self.user,
                content=self.content,
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_failure_comment_creation_without_content(self):
        with self.assertRaises(Exception):
            comment = Comment(
                product=self.product,
                user=self.user,
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_failure_comment_creation_with_empty_content(self):
        with self.assertRaises(Exception):
            comment = Comment(
                product=self.product,
                user=self.user,
                content="",
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_failure_comment_creation_with_too_long_content(self):
        # Adjust length to match your model's max_length
        long_content = "a" * 2001  # assume max_length=2000
        with self.assertRaises(Exception):
            comment = Comment(
                product=self.product,
                user=self.user,
                content=long_content,
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_failure_comment_creation_with_invalid_rating_low(self):
        # Remove if no rating field
        with self.assertRaises(Exception):
            comment = Comment(
                product=self.product,
                user=self.user,
                content=self.content,
                rating=0,  # assuming min is 1
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_failure_comment_creation_with_invalid_rating_high(self):
        # Remove if no rating field
        with self.assertRaises(Exception):
            comment = Comment(
                product=self.product,
                user=self.user,
                content=self.content,
                rating=10,  # assuming max is 5
            )
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    @log_execution
    def test_comment_string_representation(self):
        comment = Comment.objects.create(
            product=self.product,
            user=self.user,
            content=self.content,
        )
        # Adapt expectation if your __str__ differs
        expected_str_variants = {
            self.content,
            f"{self.user} - {self.product}",
            f"{self.user} - {self.content[:20]}",
        }
        self.assertIn(str(comment), expected_str_variants)
