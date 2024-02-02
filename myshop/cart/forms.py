from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=100)
    city = forms.CharField(label='Адрес', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=15)