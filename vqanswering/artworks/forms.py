from django import forms

from .models import Question_Answer


class QAForm(forms.ModelForm):
    class Meta:
        model = Question_Answer
        fields = ('title', 'question', 'answer', 'question_error_type', 'answer_error_type')
