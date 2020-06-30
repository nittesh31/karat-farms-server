from django import forms

# our new form
class ChangeTimerForm(forms.Form):
    sl_no = forms.CharField(required=True)
    start_time = forms.CharField(required=True)
    duration = forms.CharField(required=True)
    status = forms.CharField(required=True)
