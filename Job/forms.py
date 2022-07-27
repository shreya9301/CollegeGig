from django import forms
from Job.models import *
import json
import os
from collegegig.settings import MEDIA_ROOT
from taggit.forms import TagWidget


class JobForm(forms.ModelForm):
    """
      The job is poted on the Job only after moderator's approval.
    """

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['campus'].label = "Campus Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['prerequisites'].label = "Course Prerequisites :"
        self.fields['last_date'].label = "Application Deadline :"
        self.fields['org_name'].label = "Organisation Name :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Eg : Intern',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': 'Eg : 1k-5k/month',
            }
        )
        self.fields['prerequisites'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated values eg: DSA, CP ',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'Select Date',

            }
        )
        self.fields['org_name'].widget.attrs.update(
            {
                'placeholder': 'Eg: DIRD',
            }
        )

    class Meta:
        model = Job

        fields = [
            "title",
            "campus",
            "job_type",
            "salary",
            "description",
            "prerequisites",
            "last_date",
            "org_name",
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Job Type is required")
        return job_type

    def clean_campus(self):
        campus = self.cleaned_data.get('campus')

        if not campus:
            raise forms.ValidationError("Campus must be specified")
        return campus

    # Function to check whether the prerequisites written exist in the
    # university's course list or not. Done using dummy data from
    # course_data.json which represents data retrieved from University's API
    def clean_prerequisites(self):
        prerequisites = self.cleaned_data.get('prerequisites')
        f = open(os.path.join(MEDIA_ROOT, "json/course_data.json"))
        #load json data from course_data.json file
        data = json.load(f)
        course_list = data['course_list']
        course_names = [course['course_name'] for course in course_list]
        for preq in prerequisites:
            if preq not in course_names:
                raise forms.ValidationError(preq + " is not a valid course!")
        return prerequisites

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            user.save()
        return job


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']



class JobEditForm(forms.ModelForm):
    """
        Form for faculty to edit their job posted on Job
        by taking Job Title, Campus Location, Salary, Job Description,
        Application Deadline and Organisation Name as input.
    """

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['campus'].label = "Campus Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['prerequisites'].label = "Course Prerequisites :"
        self.fields['last_date'].label = "Application Deadline :"
        self.fields['org_name'].label = "Organisation Name :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Eg : Intern',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': 'Eg : 1k-5k/month',
            }
        )
        self.fields['prerequisites'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated values eg: DSA, CP ',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'Select Date',

            }
        )
        self.fields['org_name'].widget.attrs.update(
            {
                'placeholder': 'Eg: DIRD',
            }
        )

    last_date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Job Name',
        'class': 'datetimepicker1'
    }))

    class Meta:
        model = Job

        fields = [
            "title",
            "campus",
            "job_type",
            "salary",
            "description",
            "prerequisites",
            "last_date",
            "org_name",
        ]

        widgets = {
            'tags': TagWidget(),
        }

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Job Type is required")
        return job_type

    def clean_category(self):
        campus = self.cleaned_data.get('campus')

        if not campus:
            raise forms.ValidationError("category must be specified")
        return campus

    def clean_prerequisites(self):
        prerequisites = self.cleaned_data.get('prerequisites')
        with open(os.path.join(MEDIA_ROOT, "json/course_data.json")) as f:
            data = json.load(f)
            course_list = data['course_list']
            course_names = [course['course_name'] for course in course_list]
            for prerequisite in prerequisites:
                if prerequisite not in course_names:
                    raise forms.ValidationError(prerequisite + " is not a valid course!")
        return prerequisites

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
        if commit:
            user.save()
        return job

class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['job']
