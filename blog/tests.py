from django.test import TestCase
from .models import Blog
from django.urls import reverse


# class BlogModelTests(TestCase):
#     def x(self):
#         self.assertIs(1, 1)


class MyBlogsViewTests(TestCase):
    def test_unauthenticated_user_is_redirected_to_login_url(self):
        """
        If an unauthenticated user tries to access the ``my_blog`` 
        url, they should be redirected to the login page.
        """
        response = self.client.get(reverse("blog:my_blogs"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("blog:login"), response.url)

    # authenticated users see their blogs?
    def test_authenticated_user_receive_their_blogs(self):
        pass

    # authenticated users see others blogs?
    # authenticated users see "no blogs" if there's no blogs?



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


# login
    # after login, redirected to my_blogs (or other page)?
    # succesfully logged?


# other
    # what happen if (un)authenticated user try to access unexisting blogs, posts,
    # new/edit pages?
    # test images creation and delete