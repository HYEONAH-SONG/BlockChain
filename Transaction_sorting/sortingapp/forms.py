from django import forms

class TransactionForm(forms.Form):
    Transaction1 = forms.CharField()
    Transaction2 = forms.CharField()
    Transaction3 = forms.CharField()