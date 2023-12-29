from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Field
from registration.models import Question

class BasicDetailsForm(forms.Form):
    name = forms.CharField(label='First Name', max_length=100)
    gender = forms.ChoiceField(label='Gender', choices=[('M','M'),('F','F'),('O','O'),])
    registration_no = forms.CharField(label='Registraion Number', max_length=15)
    roll_no = forms.CharField(label='Roll Number', max_length=15)
    branch = forms.CharField(label='Branch', max_length=50)
    place = forms.CharField(label='Native Place', max_length=50)
    Mobile_Number = forms.CharField(label='Mobile Number', max_length=10)
    year = forms.ChoiceField(label='Year', choices=[(1,'1'),(2,'2'),])

    def __init__(self, *args, **kwargs):
        super(BasicDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'gender',
            'registration_no',
            'roll_no',
            'branch',
            'place',
            'Mobile_Number',
            'year',
            Submit('submit', 'Submit', css_class='p-2 mt-6 bg-white/10 text-white rounded-md mx-auto')
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
                self.fields[f'{question.id}'] = forms.IntegerField(label=question.question, widget=forms.widgets.NumberInput(attrs={'type': 'range', 'min': extra.get('min'), 'max': extra.get('max')}))
            elif question.type == "options":
                self.fields[f'{question.id}'] = forms.ChoiceField(label=question.question, choices=extra.get('choice'),)
        self.helper = FormHelper(self)        
        self.helper.add_input(Submit('submit', 'Submit'))

class PostsForm(forms.Form):
    comment = forms.CharField(label='', max_length=500, empty_value='Write your comment here')
    round = forms.ChoiceField(label='',choices=[(1,'Round 1'),(2,'Round 2'),(3,'Round 3')])
    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)      
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.helper.form_class = 'flex flex-wrap justify-center items-center w-full gap-4'
        self.helper.layout = Layout(
            Field('comment', css_class='border border-none rounded-xl bg-[#18191b] focus:outline-none w-80 h-12'),
            Field('round', css_class='border border-none rounded-xl bg-[#18191b] focus:outline-none focus:border-none '),
            Submit('submit', 'Comment', css_class='p-2  text-white rounded-md font-bold bg-white/10 ')
        )