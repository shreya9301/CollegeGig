from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from Job.forms import *
from Job.models import *
from Job.permission import *
import json
import os
#import re
from collegegig.settings import MEDIA_ROOT

User = get_user_model()


# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def home_view(request):

    active_jobs = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
    active_jobs_list = list(active_jobs.values())

    if request.user.is_authenticated and request.user.role == 'student':
        user_courses = request.user.get_courses()
        for i in range(len(active_jobs)):
            active_jobs_list[i]['campus_name'] = active_jobs[i].campus.get_name()
            prereqs = active_jobs[i].get_prereqs()
            matched, unmatched = [], []
            for prereq in prereqs:
                if prereq not in user_courses:
                    unmatched.append(prereq)
                else:
                    matched.append(prereq)
            active_jobs_list[i]['matched_prereqs'] = matched
            active_jobs_list[i]['unmatched_prereqs'] = unmatched
            active_jobs_list[i]['prereqs'] = prereqs
        active_jobs_list.sort(key=lambda x: -(len(x['matched_prereqs'])/(len(x['prereqs'])+0.0)) if x['prereqs'] else -1)
    else:
        for i in range(len(active_jobs)):
            active_jobs_list[i]['campus_name'] = active_jobs[i].campus.get_name()

    paginator = Paginator(active_jobs_list, 4)
    page_no = request.GET.get('page', None)
    cur_page = paginator.get_page(page_no)
    campuses = Campus.objects.all()



    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        next_page_no = cur_page.next_page_number() if cur_page.has_next() else None
        prev_page_no = cur_page.previous_page_number() if cur_page.has_previous() else None

        try:
            user_role = request.user.role
        except:
            user_role = None

        return JsonResponse({
            'page_jobs_list': cur_page.object_list,
            'cur_page_no': cur_page.number,
            'next_page_no': next_page_no,
            'no_of_page': paginator.num_pages,
            'prev_page_no': prev_page_no,
            'user_role': user_role
        })


    context = {
        'total_jobs': len(active_jobs),
        'page_jobs': cur_page,
        'campuses': campuses
    }

    return render(request, 'Job/home.html', context)


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def faculty_home_view(request):
    """
        Homepage View to display active jobs and provide search functionality
    """

    active_jobs = Job.objects.filter(is_published=True, is_closed=False, user=request.user).order_by('-timestamp')
    active_jobs_list = list(active_jobs.values())

    for i in range(len(active_jobs)):
        active_jobs_list[i]['campus_name'] = active_jobs[i].campus.get_name()

    paginator = Paginator(active_jobs_list, 4)
    page_no = request.GET.get('page', None)
    cur_page = paginator.get_page(page_no)
    campuses = Campus.objects.all()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        next_page_no = cur_page.next_page_number() if cur_page.has_next() else None
        prev_page_no = cur_page.previous_page_number() if cur_page.has_previous() else None

        try:
            user_role = request.user.role
        except:
            user_role = None

        return JsonResponse({
            'page_jobs_list': cur_page.object_list,
            'cur_page_no': cur_page.number,
            'next_page_no': next_page_no,
            'no_of_page': paginator.num_pages,
            'prev_page_no': prev_page_no,
            'user_role': user_role
        })

    context = {
        'total_jobs': len(active_jobs),
        'page_jobs': cur_page,
        'campuses': campuses,
        'user_name': request.user.first_name + " " + request.user.last_name
    }

    return render(request, 'Job/faculty_home.html', context)


def all_jobs(request):
    """
        View to display all jobs in a single container
    """

    active_jobs = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
    paginator = Paginator(active_jobs, 12)
    page_no = request.GET.get('page')
    cur_page = paginator.get_page(page_no)

    context = {
        'page_jobs': cur_page,
    }

    return render(request, 'Job/job-list.html', context)


def get_course_names():
    """
        Function to get the list of all course names from
        course_data.json
    """
    f = open(os.path.join(MEDIA_ROOT, "json/course_data.json"))
    data = dict(json.load(f))
    course_name_list = [course['course_name'] for course in data['course_list']]
    return course_name_list


def get_course_descs():
    """
        Function to get the list of all course descriptions from
        course_data.json
    """
    f = open(os.path.join(MEDIA_ROOT, "json/course_data.json"))
    data = dict(json.load(f))
    course_desc_list = [course['course_description'] for course in data['course_list']]
    return course_desc_list


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def create_job(request):
    """
    create job post
    """

    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    campuses = Campus.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for saving tags
            form.save_m2m()
            messages.success(
                request, 'Job Successfully posted! Please wait for review.')
            return redirect(reverse("Job:single-job", kwargs={
                'id': instance.id
            }))

    context = {
        'form': form,
        'campuses': campuses,
        'course_list': zip(get_course_names(), get_course_descs())
    }
    return render(request, 'Job/post-job.html', context)


def single_job(request, id):
    """
    Provide the ability to view job details
    """

    job = get_object_or_404(Job, id=id)
    context = {
        'job': job
    }
    return render(request, 'Job/single-job.html', context)


def search_result(request):
    """
        View to let students search for jobs by specifying Title,
        Organisation Name, Campus Location or Job type of their choice.
    """

    job_list = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')

    # Keywords
    if 'job_title_or_org_name' in request.GET:
        job_title_or_org_name = request.GET['job_title_or_org_name']

        if job_title_or_org_name:
            job_list = job_list.filter(title__icontains=job_title_or_org_name) | job_list.filter(
                org_name__icontains=job_title_or_org_name)

    # location
    if 'campus' in request.GET:
        campus = request.GET['campus']
        if campus:
            job_list = job_list.filter(campus=campus)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Job/search-result.html', context)


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_student
def apply_job(request, id):
    """
        View to let students apply for a particular job
        having a unique job id.
    """
    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("Job:single-job", kwargs={
                    'id': id
                }))
        else:
            return redirect(reverse("Job:single-job", kwargs={
                'id': id
            }))
    else:
        messages.error(request, 'You already applied for the Job!')
        return redirect(reverse("Job:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('Account:login'))
def dashboard(request):
    """
        Dashboard for Faculties : View their posted jobs and
        functionality to refer to applicants on that job
        Dashboard for Students : View their saved jobs and
        functionality to refer to their applied jobs
    """
    jobs = []
    saved_jobs = []
    applied_jobs = []
    total_applicants = {}

    if request.user.role == 'faculty':
        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'student':
        saved_jobs = BookmarkJob.objects.filter(user=request.user.id)
        applied_jobs = Applicant.objects.filter(user=request.user.id)

    context = {
        'jobs': jobs,
        'saved_jobs': saved_jobs,
        'applied_jobs': applied_jobs,
        'total_applicants': total_applicants
    }

    return render(request, 'Job/dashboard.html', context)


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def delete_job(request, id):
    """
        User functionality to delete a job
    """
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Job Post deleted successfully!')

    return redirect('Job:dashboard')


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def job_complete(request, id):
    """
        User functionality to mark a job as closed
    """
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')

    return redirect('Job:dashboard')


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def all_applicants(request, id):
    """
    View to display all applicants of given job id
    """
    all_applicants = Applicant.objects.filter(job=id)
    job = Job.objects.get(id=id)
    prereqs = job.get_prereqs()
    all_applicants_grades = []
    for applicant in all_applicants:
        all_applicants_grades.append([str(course + " : " + applicant.user.get_grade(course)) for course in prereqs])
    context = {
        'all_applicants': zip(all_applicants, all_applicants_grades)
    }

    return render(request, 'Job/all-applicants.html', context)


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def applicant_details(request, id):
    """
        View Details of Applicant ( Name, Email and Transcript )
    """
    applicant = get_object_or_404(User, id=id)
    applicant_transcript = applicant.get_transcript()

    context = {
        'applicant': applicant,
        'applicant_transcript': applicant_transcript
    }

    return render(request, 'Job/applicant-details.html', context)


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_student
def bookmark_job_view(request, id):
    """
        Bookmark Job with given id
    """
    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'Job saved successfully!')
                return redirect(reverse("Job:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("Job:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("Job:single-job", kwargs={
            'id': id
        }))

def delete_bookmark(request, id):
    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:
        job.delete()

    return redirect('Job:dashboard')


@login_required(login_url=reverse_lazy('Account:login'))
@user_is_faculty
def job_edit(request, id=id):

    job = get_object_or_404(Job, id=id)
    campuses = Campus.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        form.save_m2m()
        messages.success(request, 'Your Job Post was Successfully Updated!')
        return redirect(reverse("Job:single-job", kwargs={
            'id': instance.id
        }))
    context = {
        'form': form,
        'campuses': campuses,
        'course_list': zip(get_course_names(), get_course_descs())
    }

    return render(request, 'Job/job-edit.html', context)