from django.contrib.auth.forms import UserCreationForm
from .models import User,Question, Choice
from django.forms import ModelForm

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email')


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        """widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 5}),
        }"""

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        exclude = ['votes']