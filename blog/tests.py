from django.test import TestCase
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth import get_user_model, get_user
from .models import Blog, Post


User = get_user_model()


class UnauthenticatedUserIsRedirectedToLogin(TestCase):
    # melhor remover test
    def test_unauthenticated_user_is_redirected_to_login(self):
        if self.__class__.__name__ != 'UnauthenticatedUserIsRedirectedToLogin':
            response = self.client.get(self.url)
            query_string = urlencode({'next': self.url})
            login_url = reverse("accounts:login")
            self.assertRedirects(response, f"{login_url}?{query_string}")


# class IndexViewTests


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

    def test_unauthenticated_user_is_redirected_to_login(self):
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

        # Ensures that exists 3 users.
        self.assertEqual(len(User.objects.all()), 3)

class NewBlogViewTests(TestCase):
    def test_there_is_no_users_created(self):
        self.assertEqual(len(User.objects.all()), 0)

    def test_unauthenticated_user_is_redirected_to_login(self):
        new_blog_url = reverse("blog:new_blog")
        response = self.client.get(new_blog_url)
        query_string = urlencode({'next': new_blog_url})
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?{query_string}")

        #post
        #n logado;tentar criar blog;redirect to login;login;redir to myblogs?
    
    # mudar nomes dos testes; user_get, user_post, etc...
    def test_new_blog_is_associated_to_correct_user(self):
        user = User.objects.create_user(
            username='Testuser',
            email='testemail@example.com',
            password='mypassword123')
        
        # Ensures blogs were created.
        self.client.force_login(user)
        new_blog_url = reverse("blog:new_blog")
        self.assertEqual(user.blog_set.count(), 0)
        response = self.client.post(new_blog_url, data={'title': "Title"}) # testar se o blog tem realmente esse title?
        self.assertEqual(user.blog_set.count(), 1)

        # Ensures that after creating the blog, it is 
        # successfully redirected to my_blogs.
        my_blogs_url = reverse("blog:my_blogs")
        self.assertRedirects(response, my_blogs_url)

        # Ensures created blogs are acessible.
        response = self.client.get(my_blogs_url)
        blogs = user.blog_set.all()
        self.assertCountEqual(
            blogs.values_list('id', flat=True),
            response.context['blogs'].values_list('id', flat=True))
        
        # test with 2 blogs?


class EditBlogViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='Testuser',
            email='testemail@example.com',
            password='mypassword123')
        cls.user2 = User.objects.create_user(
            username='Testuser2',
            email='testemail2@example.com',
            password='mypassword123')
        cls.blog = Blog.objects.create(user=cls.user, title='Test') # cls.user blog.
        cls.blog2 = Blog.objects.create(user=cls.user2, title='Test2') # cls.user2 blog.
        # Url for editing cls.blog.
        cls.edit_blog_url = reverse("blog:edit_blog", kwargs={"blog_id": cls.blog.id})
        # Url for editing cls.blog2.
        cls.edit_blog_url2 = reverse("blog:edit_blog", kwargs={"blog_id": cls.blog2.id})

    def test_unauthenticated_user_is_redirected_to_login(self):
        response = self.client.get(self.edit_blog_url)
        query_string = urlencode({'next': self.edit_blog_url})
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?{query_string}")

    def test_authenticated_user_can_get_his_blog_edit_page(self): # fazer 1 só para get e post? trying_acess_to
        self.client.force_login(self.user)
        response = self.client.get(self.edit_blog_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_post_on_his_blog_edit_page(self):
        self.client.force_login(self.user)
        response = self.client.post(self.edit_blog_url, data={'title': 'Edited test'})
        my_blogs_url = reverse("blog:my_blogs")
        self.assertRedirects(response, my_blogs_url)

        # Check if title really changed.
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, 'Edited test')

    def test_authenticated_user_cant_get_others_blog_edit_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.edit_blog_url2)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_cant_post_on_others_blog_edit_page(self):
        self.client.force_login(self.user)
        response = self.client.post(self.edit_blog_url2, data={'title': 'Edited title'})
        self.assertEqual(response.status_code, 404)

        # Check if title really did not change.
        self.blog2.refresh_from_db()
        self.assertEqual(self.blog2.title, 'Test2')
        
    def test_authenticated_user_cant_get_nonexistent_blog_edit_page(self):
        self.client.force_login(self.user)
        blog_id = 3 # A nonexistent blog id.
        response = self.client.get(reverse('blog:edit_blog', kwargs={'blog_id': blog_id}))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_cant_post_on_nonexistent_blog_edit_page(self):
        self.client.force_login(self.user)
        nonexistent_blog_id = 3
        nonexistent_blog_url = reverse(
            'blog:edit_blog', kwargs={'blog_id': nonexistent_blog_id})
        response = self.client.post(
            nonexistent_blog_url, data={'title': 'Test'})
        self.assertEqual(response.status_code, 404)


class PostsViewTests(UnauthenticatedUserIsRedirectedToLogin):
    @classmethod
    def setUpTestData(cls):
        # User 1.
        cls.user = User.objects.create_user(
            username='Testuser',
            email='testemail@example.com',
            password='mypassword123')
        cls.blog = Blog.objects.create(user=cls.user, title='Test')
        cls.url = reverse("blog:posts", kwargs={'blog_id': cls.blog.id})
        # User 2.
        cls.user2 = User.objects.create_user(
            username='Testuser2',
            email='testemail2@example.com',
            password='mypassword123')

    def test_authenticated_user_one_post(self):
        Post.objects.create(blog=self.blog, title='Test', text='Test') # após fazer isso existe 1 post?
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            Post.objects.values_list("id", flat=True),
            response.context['posts'].values_list("id", flat=True))
        
    def test_authenticated_user_two_posts(self):
        Post.objects.create(blog=self.blog, title='Test', text='Test')
        Post.objects.create(blog=self.blog, title='Test', text='Test') # Existem 2 posts?
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            Post.objects.values_list("id", flat=True),
            response.context['posts'].values_list("id", flat=True))

    def test_authenticated_user_cant_see_other_user_posts(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_with_no_blogs(self):
        blog = Blog.objects.create(user=self.user2, title='Test')
        posts_url = reverse("blog:posts", kwargs={'blog_id': blog.id})
        self.client.force_login(self.user2)
        response =  self.client.get(posts_url)
        self.assertContains(response, 'No posts added...')

    def test_authenticated_user_cant_access_posts_from_nonexisting_blog(self):
        blog_id = 2 # blog realmente não existe?
        posts_url = reverse("blog:posts", kwargs={'blog_id': blog_id})
        self.client.force_login(self.user2)
        response =  self.client.get(posts_url)
        self.assertEqual(response.status_code, 404)


class NewPostViewTests(UnauthenticatedUserIsRedirectedToLogin):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='Testuser',
            email='testemail@example.com',
            password='mypassword123')
        cls.blog = Blog.objects.create(user=cls.user, title='Test')
        cls.url = reverse('blog:new_post', kwargs={'blog_id': cls.blog.id})
        cls.user2 = User.objects.create_user(
            username='Testuser2',
            email='testemail2@example.com',
            password='mypassword123')
        cls.posts_url = reverse("blog:posts", kwargs={'blog_id': cls.blog.id})
        cls.post_data = {'title': 'Test', 'text': 'Test'}

    # no post test for unauthenticated user #
        
    def test_owner_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_owner_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.post_data)
        self.assertRedirects(response, self.posts_url)

    def test_authenticated_user_one_post(self):
        self.client.force_login(self.user)
        self.client.post(self.url, data=self.post_data)
        self.assertEqual(Post.objects.filter(blog__user=self.user).count(), 1)
    
    def test_two_posts(self):
        self.client.force_login(self.user)
        self.client.post(self.url, data=self.post_data)
        self.client.post(self.url, data=self.post_data)
        self.assertEqual(Post.objects.filter(blog__user=self.user).count(), 2)

    def test_authenticated_user_get_other_user_new_post_page(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_post_other_user_new_post_page(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_get_new_post_page_for_nonexistent_blog(self):
        self.client.force_login(self.user)
        nonexistent_blog_id = 2 # setuptestdata?
        new_post_url_for_nonexistent_blog = reverse( # setuptestdata?
            'blog:new_post', kwargs={'blog_id': nonexistent_blog_id}
            )
        response = self.client.get(new_post_url_for_nonexistent_blog)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_post_new_post_page_for_nonexistent_blog(self):
        self.client.force_login(self.user)
        nonexistent_blog_id = 2
        new_post_url_for_nonexistent_blog = reverse(
            'blog:new_post', kwargs={'blog_id': nonexistent_blog_id}
            )
        response = self.client.post(
            new_post_url_for_nonexistent_blog, data=self.post_data
            )
        self.assertEqual(response.status_code, 404)


class EditPostViewTests(UnauthenticatedUserIsRedirectedToLogin):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='Testuser',
            email='testemail@example.com',
            password='mypassword123')
        cls.blog = Blog.objects.create(user=cls.user, title='Test')
        cls.post = Post.objects.create(blog=cls.blog, title='Test', text='Test')
        cls.edit_post_url = reverse('blog:edit_post', kwargs={'post_id': cls.post.id})
        cls.url = cls.edit_post_url
        cls.post_data = {'title': 'Test', 'text': 'Test'}
        cls.post_data_edited = {'title': 'Edited', 'text': 'Edited'}
        cls.posts_url = reverse('blog:posts', kwargs={'blog_id': cls.blog.id})
        cls.non_owner = User.objects.create_user(
            username='Testuser2',
            email='testemail2@example.com',
            password='mypassword123')

    def test_owner_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_owner_post(self):
        self.client.force_login(self.user)
        # talvez melhor criar post aqui #
        response = self.client.post(self.url, data=self.post_data)
        self.assertRedirects(response, self.posts_url)

    def test_edited(self):
        self.client.force_login(self.user)
        # talvez melhor criar post aqui #
        self.client.post(self.url, data=self.post_data_edited)
        self.post.refresh_from_db()
        self.assertEqual(
            (self.post.title, self.post.text),
            (self.post_data_edited['title'], self.post_data_edited['text']))

    def test_non_owner_get(self):
        self.client.force_login(self.non_owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_non_owner_post(self):
        self.client.force_login(self.non_owner)
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, 404)

    # get nonexisting post # qual erro deve ser retornado?

    # post nonexisting post # qual erro deve ser retornado?

    # COMMIT!!!!
    


    # other
        # Para os métodos que não deveriam ser aceitos, pode ser útil garantir que o servidor responde com 405 Method Not Allowed ou 403 Forbidden, principalmente em APIs (Django REST Framework, por exemplo).