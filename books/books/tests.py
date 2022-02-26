from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from .models import Book, Review



class BookTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title='Harry Potter', author='JK Rowling', price='25.00')
        self.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='reviewuser@email.com',
            password='testpass123'
        )
        self.special_permission = Permission.objects.get(codename='special_status')
        self.review = Review.objects.create(
            author=self.user,
            book=self.book,
            review='An excellent review'
        )

    
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('account_login')
        book_list_url = reverse('book_list')
        self.assertRedirects(response, f'{login_url}?next={book_list_url}')
        response = self.client.get(f'{login_url}?next={book_list_url}')
        self.assertContains(response, 'login')

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertEqual(response.context['book'], self.book)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, 'An excellent review')

