from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from registration.models import Question

class BasicDetailsForm(forms.Form):
    name = forms.CharField(label='First Name', max_length=100)
    email = forms.EmailField(label='Email')
    gender = forms.ChoiceField(label='gender', choices=[('M','M'),('F','F'),('O','O'),])
    registration_no = forms.CharField(label='Registraion Number', max_length=15)
    roll_no = forms.CharField(label='Roll Number', max_length=15)
    branch = forms.CharField(label='Branch', max_length=15)
    place = forms.CharField(label='Native Place', max_length=50)

    def __init__(self, *args, **kwargs):
        super(BasicDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'email',
            'gender',
            'registration_no',
            'roll_no',
            'branch',
            'place',
            Submit('submit', 'Submit', css_class='my-2 px-4 py-2 bg-green-500 text-white rounded-md')
        )

class QuestionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionsForm, self).__init__(*args, **kwargs)
        questions = Question.objects.all()
        for question in questions:
            if question.additional_data is not None:
                extra = question.additional_data
            if question.type == "text":
                self.fields[f'{question.id}'] = forms.CharField(label=question.question, max_length=500)
            elif question.type == "range":
                self.fields[f'{question.id}'] = forms.IntegerField(        label=question.question, widget=forms.widgets.NumberInput(attrs={'type': 'range', 'min': extra.get('min'), 'max': extra.get('max')}))
                # self.fields[f'{question.id}'] = forms.IntegerField(        label=question.question, min_value= extra.get('min'), max_value= extra.get('max'))
            elif question.type == "options":
                self.fields[f'{question.id}'] = forms.ChoiceField(label=question.question, choices=extra.get('choice'),)
        self.helper = FormHelper(self)        
        self.helper.add_input(Submit('submit', 'Submit'))

    