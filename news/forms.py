from   django import forms
from django.utils.text import slugify

from  .models import Contact,Category,Comments,News
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm




class AddNewsForm(forms.ModelForm):
    class Meta:
        model=News
        fields=('title','category','image','body','publish_time','status')

    #
    # def seve(self,commit=True):
    #     instance=super().save(commit=False)
    #     instance.slug=slugify(instance.title)
    #     if commit:
    #         instance.save()
    #     return instance

    def save(self, commit=True):
        instance=super().save(commit=False)
        instance.slug=slugify(instance.title)
        if commit:
            instance.save()
            return instance


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'



