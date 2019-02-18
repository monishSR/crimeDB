from django import forms


class SearchForm(forms.Form):
    Search = forms.CharField(required=True, max_length=100, help_text='100 characters max.')


class entryForm(forms.Form):
    First_Name = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    Middle_Name = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    Last_Name = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    SSN = forms.CharField(required=True, max_length=9, help_text='eg: E01002000')
    DOB = forms.DateField(required=True, )
    Sex = forms.CharField(required=True, max_length=1, help_text='F/M')
    Height = forms.FloatField(required=True, help_text='In feet')
    Weight = forms.IntegerField(required=True, help_text='In kg')
    Hair_Colour = forms.CharField(required=False, max_length=20, help_text='20 characters max.')
    Distinct_Mark = forms.CharField(required=False, max_length=30, help_text='30 characters max.')
    Address = forms.CharField(required=True, max_length=30, help_text='30 characters max.')
    Occupation = forms.CharField(required=False, max_length=30, help_text='30 characters max.')

    Detective_ID = forms.IntegerField(required=True, help_text='eg: 50000')

    Dependent_fname = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    Dependent_lname = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    Dependent_relationship = forms.CharField(required=True, max_length=20, help_text='20 characters max.')
    Dependent_contactno = forms.IntegerField(required=True, help_text='eg: 2489512')

    Case_ID = forms.IntegerField(required=True, help_text='eg: 2734')
    Case_crime = forms.IntegerField(required=True, help_text='1-61')
    Case_description = forms.CharField(required=True, max_length=70, help_text='70 characters max.')
    Case_location = forms.CharField(required=True, max_length=30, help_text='30 characters max.')
