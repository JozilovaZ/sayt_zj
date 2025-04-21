from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .models import Category, News, Comments, Contact
from datetime import timedelta
from .views import home_page,seach_new_page,new_detail_page,sport_page_view,xorij_page_view,mahalliy_page_view,texnologiya_page_view,addnew_view,add_category_view,add_news_with_tags,contact_page_view,register,LogoutView,LoginView


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Technology")
        self.assertEqual(category.name, "Technology")
        self.assertTrue(category.created_at)
        self.assertEqual(str(category), "Technology")

    def test_category_unique_name(self):
        Category.objects.create(name="Technology")
        with self.assertRaises(Exception):
            Category.objects.create(name="Technology")


class NewsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Technology")
        self.news = News.objects.create(
            title="Test News",
            category=self.category,
            slug="test-news",
            body="This is a test news body.",
            status=News.Status.Published,
            publish_time=timezone.now()
        )

    def test_news_creation(self):
        self.assertEqual(self.news.title, "Test News")
        self.assertEqual(self.news.category, self.category)
        self.assertEqual(self.news.slug, "test-news")
        self.assertEqual(self.news.status, News.Status.Published)
        self.assertEqual(self.news.view_count, 0)
        self.assertTrue(self.news.created_at)
        self.assertTrue(self.news.updated_at)
        self.assertEqual(str(self.news), "Test News")

    def test_published_manager(self):
        draft_news = News.objects.create(
            title="Draft News",
            category=self.category,
            slug="draft-news",
            body="Draft body",
            status=News.Status.Draft
        )
        published_news = News.published.all()
        self.assertIn(self.news, published_news)
        self.assertNotIn(draft_news, published_news)

    def test_ordering(self):
        older_news = News.objects.create(
            title="Older News",
            category=self.category,
            slug="older-news",
            body="Older body",
            status=News.Status.Published,
            publish_time=timezone.now() - timedelta(days=1)
        )
        news_list = News.published.all()
        self.assertEqual(news_list[0], self.news)  # Newer news comes first

    def test_tags(self):
        self.news.tags.add("tech", "innovation")
        self.assertIn("tech", self.news.tags.names())
        self.assertIn("innovation", self.news.tags.names())


class CommentsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Technology")
        self.news = News.objects.create(
            title="Test News",
            category=self.category,
            slug="test-news",
            body="This is a test news body.",
            status=News.Status.Published
        )
        self.comment = Comments.objects.create(
            user=self.user,
            new=self.news,
            comment="Great news!",
            status=Comments.Status.Published
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.new, self.news)
        self.assertEqual(self.comment.comment, "Great news!")
        self.assertEqual(self.comment.status, Comments.Status.Published)
        self.assertTrue(self.comment.created_at)
        self.assertEqual(str(self.comment), f"{self.user} - {self.news} - Great news!")

    def test_published_manager(self):
        draft_comment = Comments.objects.create(
            user=self.user,
            new=self.news,
            comment="Draft comment",
            status=Comments.Status.Draft
        )
        published_comments = Comments.published.all()
        self.assertIn(self.comment, published_comments)
        self.assertNotIn(draft_comment, published_comments)

    def test_ordering(self):
        older_comment = Comments.objects.create(
            user=self.user,
            new=self.news,
            comment="Older comment",
            status=Comments.Status.Published,
            created_at=timezone.now() - timedelta(days=1)
        )
        comment_list = Comments.published.all()
        self.assertEqual(comment_list[0], self.comment)  # Newer comment comes first


class ContactModelTest(TestCase):
    def test_contact_creation(self):
        contact = Contact.objects.create(
            full_name="John Doe",
            email="john@example.com",
            supject="Test Subject",
            message="This is a test message."
        )
        self.assertEqual(contact.full_name, "John Doe")
        self.assertEqual(contact.email, "john@example.com")
        self.assertEqual(contact.supject, "Test Subject")
        self.assertEqual(contact.message, "This is a test message.")
        self.assertTrue(contact.created_at)
        self.assertEqual(str(contact), "This is a test message.")


class PublishedManagerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Technology")
        self.published_news = News.objects.create(
            title="Published News",
            category=self.category,
            slug="published-news",
            body="Published body",
            status=News.Status.Published
        )
        self.draft_news = News.objects.create(
            title="Draft News",
            category=self.category,
            slug="draft-news",
            body="Draft body",
            status=News.Status.Draft
        )

    def test_published_manager_news(self):
        published = News.published.all()
        self.assertIn(self.published_news, published)
        self.assertNotIn(self.draft_news, published)