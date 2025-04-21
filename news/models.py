from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class PublishedManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.Status.Published)




class Category(models.Model):
    name=models.CharField(max_length=200,null=False,blank=False,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class News(models.Model):

    class Status(models.TextChoices):
        Draft="DF","Draft"
        Published="PB","Published"


    title=models.CharField(max_length=200,null=False,blank=False, help_text="Yangilikning sarlovhasi")
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=200)
    image=models.ImageField(upload_to='image_in/',null=True,blank=True)
    body=RichTextUploadingField()
    view_count=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    publish_time=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.Draft)
    objects=models.Manager()    #standart
    published=PublishedManger()
    tags = TaggableManager()

    class Meta:
        ordering=["-publish_time"]

    def __str__(self):
        return self.title



class Comments(models.Model):
    class Status(models.TextChoices):
        Draft = "DF", "Draft"
        Published = "PB", "Published"

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    new=models.ForeignKey(News,on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.Published)
    objects = models.Manager()
    published = PublishedManger()
    class Meta:
        ordering=["-created_at"]


    def __str__(self):
        return f"{self.user} - {self.new} -{self.comment}"




class Contact(models.Model):
    full_name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField()
    supject=models.CharField(max_length=100,null=True,blank=True)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
