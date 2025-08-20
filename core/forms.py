from django import forms
from .models import Post
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if pwd and confirm and pwd != confirm:
            raise forms.ValidationError("Passwords do not match.")


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    login_input = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'What’s happening?',
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 rounded p-1'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 rounded p-1'
            }),
        }





# forms.py
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['image', 'bio']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Exclude the current user when checking for duplicates
            if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
                raise forms.ValidationError("This email is already in use.")
        return email
