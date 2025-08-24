from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import User


class Blog(models.Model):
    """A blog."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='', default='no_img.png')
    profile_image = models.ImageField(upload_to='', default='no_img.png')
    background_image = models.ImageField(upload_to='', default='no_img.png')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
    
    def delete(self, *args, **kwargs):
        for image in self.cover_image, self.profile_image, self.background_image:
            if image:
                if os.path.isfile(image.path):
                    if image.path != os.path.join(settings.MEDIA_ROOT, 'no_img.png'):
                        os.remove(image.path)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            blog = Blog.objects.get(pk=self.pk)
            images = (
                (blog.cover_image, self.cover_image),
                (blog.profile_image, self.profile_image),
                (blog.background_image, self.background_image),
            )
            # old_images = blog.cover_image, blog.profile_image, blog.background_image
            # current_images = self.cover_image, self.profile_image, self.background_image
            for old, new in images:
                if new != old != 'no_img.png':
                    os.remove(old.path)

            # for image, image2 in current_images, old_images:
            #     if image not in old_images: # att img
            #         if image != 'no_img.png':
            #             os.remove(image.path)
        except Blog.DoesNotExist:
            pass
        return super().save(*args, **kwargs)


class Post(models.Model):
    """A blog post."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', default='no_img.png')
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                if self.image.path != os.path.join(settings.MEDIA_ROOT, 'no_img.png'):
                    os.remove(self.image.path)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            imagem_anterior = Post.objects.get(pk=self.pk).image
            if self.image != imagem_anterior:
                if imagem_anterior != 'no_img.png':
                    os.remove(imagem_anterior.path)
        except Post.DoesNotExist:
            pass
        return super().save(*args, **kwargs)
