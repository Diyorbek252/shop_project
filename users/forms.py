from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
import re
from datetime import date
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class RegistorForm(UserCreationForm):
    phone_number = forms.CharField(
        label="Telefon raqami",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+998901234567'})
    )
    date_of_birth = forms.DateField(
        label="Tug'ilgan sana",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields =  UserCreationForm.Meta.fields + ('email', 'phone_number', 'date_of_birth', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            phone = phone.strip()
            # +998901234567 yoki 998901234567 yoki 901234567 formatlarini qabul qiladi
            pattern = r'^(\+?998)?[0-9]{9}$'
            if not re.match(pattern, phone):
                raise ValidationError("Telefon raqami noto'g'ri formatda. Masalan: +998901234567")

            # Har doim bir xil formatga keltirib saqlash (+998901234567)
            digits = re.sub(r'\D', '', phone)
            if digits.startswith('998') and len(digits) == 12:
                phone = f'+{digits}'
            elif len(digits) == 9:
                phone = f'+998{digits}'
            else:
                phone = f'+{digits}'
        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            if dob > today:
                raise ValidationError("Tug'ilgan sana kelajakda bo'lishi mumkin emas.")
            if age < 13:
                raise ValidationError("Ro'yxatdan o'tish uchun kamida 13 yoshda bo'lishingiz kerak.")
            if age > 120:
                raise ValidationError("Tug'ilgan sana noto'g'ri kiritilgan.")
        return dob