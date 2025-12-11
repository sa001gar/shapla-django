from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_ckeditor_5.fields import CKEditor5Field
import sys

# Create your models here.

"""
Model: Category
Fields:
    name: str
    slug: str
    description: str
    created_at: datetime
    updated_at: datetime
"""
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

def compress_image(image_field, max_size=(800, 800)):
    if not image_field:
        return

    img = Image.open(image_field)
    
    # Handle transparency (RGBA) -> RGB with white background
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail(max_size, Image.LANCZOS)

    output = BytesIO()
    img.save(output, format='JPEG', quality=70)
    output.seek(0)

    image_field.file = InMemoryUploadedFile(
        output,
        'ImageField',
        f"{image_field.name.split('.')[0]}.jpg",
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )

""" Model : Author
Fields:
    name: str
    slug: str
    description: str
    created_at: datetime
    updated_at: datetime
"""
class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    author_image = models.ImageField(upload_to='author_images', blank=True, null=True)
    author_image_alt = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.author_image:
            if not self.pk:
                # New instance, compress image
                compress_image(self.author_image)
            else:
                # Existing instance, check if image changed
                try:
                    this = Author.objects.get(id=self.id)
                    if this.author_image != self.author_image:
                        compress_image(self.author_image)
                except Author.DoesNotExist:
                    # Should not happen if pk exists, but safe fallback
                    compress_image(self.author_image)
                    
        super(Author, self).save(*args, **kwargs)

"""
Model: Post
Fields:
    title: str
    slug: str
    description: str
    created_at: datetime
    updated_at: datetime
"""
class Post(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    
    post_image = models.ImageField(upload_to='post_images', blank=True, null=True)
    post_image_alt = models.CharField(max_length=100, blank=True)
    post_text = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.post_image:
            if not self.pk:
                # New instance, compress
                compress_image(self.post_image)
            else:
                 # Existing instance, check if image changed
                try:
                    this = Post.objects.get(id=self.id)
                    if this.post_image != self.post_image:
                        compress_image(self.post_image)
                except Post.DoesNotExist:
                    compress_image(self.post_image)
                    
        super(Post, self).save(*args, **kwargs)

"""
Model : TeamMember
Fields:
    name: str
    slug: str
    role: str
    created_at: datetime
    updated_at: datetime
"""
class TeamMember(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    role = models.CharField(max_length=100, blank=True)
    team_image = models.ImageField(upload_to='team_member_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['name']

    def __str__(self):
        return self.name