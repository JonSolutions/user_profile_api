from django import forms
from .models import GenderModel, CourseMajorModel, PasswordResetModel


class StudentForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'required': 'required'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            'required': 'required'
        })
    )

    email = forms.EmailField(
        help_text="We'll never share your email with anyone else.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'required': 'required'
        })
    )

    reg_no = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registration number',
            'required': 'required'
        })
    )

    id_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your ID number',
            'required': 'required'
        })
    )

    age = forms.IntegerField(
        min_value=16,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age',
            'required': 'required'
        })
    )

    course = forms.ModelChoiceField(
        queryset=CourseMajorModel.objects.all(),
        empty_label="Select Course",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

    gender = forms.ModelChoiceField(
        queryset=GenderModel.objects.all(),
        empty_label="Select Gender",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )


class CourseModelForm(forms.ModelForm):
    class Meta:
        model = CourseMajorModel
        fields = '__all__'

class GenderModelForm(forms.ModelForm):
    class Meta:
        model = GenderModel
        fields = '__all__'

class PasswordResetModelForm(forms.ModelForm):
    class Meta:
        model = PasswordResetModel
        fields = '__all__'


#user profile api app model forms

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from user_profile_api_app.models import User, Profile


class UserRegistrationForm(UserCreationForm):
    """Custom form for user registration with email as username"""

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(PasswordResetForm):
    """Custom form for password reset functionality"""

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("There is no user registered with this email address."))
        return email


class ProfileForm(forms.Form):
    """Form for Profile model without direct model inheritance"""

    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 4})
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'})
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'})
    )

    def save(self, user, commit=True):
        """Save profile data for a given user"""
        profile, created = Profile.objects.get_or_create(user=user)
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.bio = self.cleaned_data['bio']
        profile.birth_date = self.cleaned_data['birth_date']
        if self.cleaned_data.get('profile_picture'):
            profile.profile_picture = self.cleaned_data['profile_picture']
        profile.location = self.cleaned_data['location']
        profile.website = self.cleaned_data['website']
        profile.phone_number = self.cleaned_data['phone_number']

        if commit:
            profile.save()
        return profile


class GenderForm(forms.Form):
    """Form for Gender model without direct model inheritance"""

    gender = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gender'})
    )

    def save(self, commit=True):
        """Save gender data"""
        gender = GenderModel(
            gender=self.cleaned_data['gender']
        )
        if commit:
            gender.save()
        return gender


class CourseMajorForm(forms.Form):
    """Form for Course Major model without direct model inheritance"""

    course_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'})
    )
    course_code = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'})
    )

    def save(self, commit=True):
        """Save course major data"""
        course = CourseMajorModel(
            course_name=self.cleaned_data['course_name'],
            course_code=self.cleaned_data['course_code']
        )
        if commit:
            course.save()
        return course


class PasswordResetRequestForm(forms.Form):
    """Custom form for requesting password reset without direct model inheritance"""

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("No user with this email address exists."))
        return email




class CustomLoginForm(AuthenticationForm):
    """
    Custom login form that uses email as the username field
    """
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'autofocus': True
        })
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
    )

    remember_me = forms.BooleanField(
        label=_("Remember me"),
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = self.authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def authenticate(self, request, username=None, password=None):
        from django.contrib.auth import authenticate
        return authenticate(request=request, username=username, password=password)

    def get_user(self):
        return self.user_cache
