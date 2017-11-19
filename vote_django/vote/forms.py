from django.contrib.auth.forms import UserCreationForm
from .models import User,Question
from django.forms import ModelForm,Textarea

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email')


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 5}),
        }