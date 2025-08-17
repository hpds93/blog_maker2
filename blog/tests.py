from django.test import TestCase
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth import get_user_model, get_user
from .models import Blog


User = get_user_model()


class MyBlogsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 3 users.
        cls.user = User.objects.create_user(
            username='Testuser',
            email='testemail@example.com',
            password='mypassword123')
        cls.user2 = User.objects.create_user(
            username='Testuser2',
            email='testemail2@example.com',
            password='mypassword123')
        cls.user3 = User.objects.create_user(
            username='Testuser3',
            email='testemail3@example.com',
            password='mypassword123')
        
        # Create 3 blogs for user and user2.
        # user3 has no blogs.
        for user in cls.user, cls.user2:
            for _ in range(3):
                Blog.objects.create(user=user, title='Test')

    def test_unauthenticated_user_is_redirected_to_login_url(self):
        # Ensures that no user is logged in.
        self.client.logout()
        self.assertIsNone(self.client.session.get("_auth_user_id"))

        my_blogs_url = reverse("blog:my_blogs")
        response = self.client.get(my_blogs_url)
        query_string = urlencode({'next': my_blogs_url})
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?{query_string}")

    def test_authenticated_user_receive_correct_blogs(self):
        for user, n_blogs in ((self.user, 3), (self.user2, 3), (self.user3, 0)):
            # Ensures that a new user has logged in.
            self.client.logout()
            self.client.force_login(user)
            self.assertEqual(user, get_user(self.client))

            # Ensures that the user has the expected number of blogs.
            blogs = Blog.objects.filter(user=user)
            self.assertEqual(len(blogs), n_blogs)

            response = self.client.get(reverse("blog:my_blogs"))

            # Ensures that the QuerySet object provided by the view’s 
            # context has the expected number of blogs.
            self.assertEqual(len(response.context['blogs']), n_blogs)

            # Ensures that the number of user blogs matches the number
            # of blogs provided in the view’s context, and that they 
            # have the same IDs.        
            self.assertCountEqual(
                blogs.values_list("id", flat=True),
                response.context['blogs'].values_list("id", flat=True))
        
        # Ensures that a total of 6 blogs were created.
        self.assertEqual(len(Blog.objects.all()), 6)

        # Ensures tha the user with no blogs see the correct message.
        self.assertContains(response, 'No blogs added...')


#commit
# new_blog
    # unauthenticated user receives 404? redirected to login?
    # authenticated user can create blog for other user? permissions?
    # new blogs are vinculated to an user?


# edit_blog
    # unauthenticated user receives 404? redirected to login?
    # authenticated user can edit blog for other user? permissions?


# posts
    # unauthenticated user receives 404? redirected to login?
    # authenticated user can acess posts from other users? should have permission system?
    # blogs with no posts?


# new_post
    # unauthenticated user receives 404? redirected to login?
    # authenticated user can create posts for other users? should have permission system?

    # posts are vinculated to blogs?
    # posts are vinculated to the correct blog an user?
    # each blog have a different version of new_post url [IMPORTANT]


# edit post
    # unauthenticated user receives 404? redirected to login?
    # authenticated user can edit posts for other users? should have permission system?

    # are the user editing the correct blog's post?
    # each blog have a different version of edit_post url [IMPORTANT]


# register
    # after registering, the system automatically creates a Blog instance for the user?
    # after registering, the system automatically login the user?
    # succesfully registered?
    # create first blog automatically?


# login
    # login redireciona onde?
    # se redirecionado para login, pra onde sou redirecionado depois? para o redirecionamento normal de login, ou para a url que tentei acessar antes de estar logado?
    # after login, redirected to my_blogs (or other page)?
    # succesfully logged?


# other
    # what happen if (un)authenticated user try to access unexisting blogs, posts,
    # new/edit pages?
    # test images creation and delete