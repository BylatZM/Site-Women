from django import forms
from django.forms import ValidationError
from . import models

class AddPostForm(forms.ModelForm):
  cat = forms.ModelChoiceField(queryset=models.Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
  husband = forms.ModelChoiceField(queryset=models.Husband.objects.all(), required=False, empty_label="Не замужем", label="Муж")

  class Meta:
    model = models.Women
    fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input'}),
      'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
    }
    labels = {'slug': 'URL'}

  def clean_title(self):
    title = self.cleaned_data['title']
    if len(title) > 50:
      raise ValidationError("Длинна превышает 50 символов")
    
    return title

class UploadFileForm(forms.Form):
  #file = forms.FileField(label="Файл")
  file = forms.ImageField(label="Файл")