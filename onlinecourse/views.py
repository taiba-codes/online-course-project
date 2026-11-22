from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def popular_course_list(request):
    context = {}
    if request.method == 'GET':
        # Create sample course and lesson safely using exact model fields
        c, created = Course.objects.get_or_create(
            name="Django Cloud Application Development",
            defaults={"description": "Learn Django step by step."}
        )
        Lesson.objects.get_or_create(
            title="Introduction to Django",
            course=c
        )

        course_list = Course.objects.order_by('-id')[:10]
        context['course_list'] = course_list
        context['course'] = c
        return render(request, 'onlinecourse/course_details_bootstrap.html', context)

def course_details(request, course_id):
    context = {}
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            context['course'] = course
            return render(request, 'onlinecourse/course_details_bootstrap.html', context)
        except Course.DoesNotExist:
            raise Http404("Course not found")

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        if request.user.is_authenticated:
            enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
            enrollment.mode = 'audit'
            enrollment.save()
        return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        selected_ids = request.POST.getlist('choice')
        if request.user.is_authenticated:
            enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
            submission = Submission.objects.create(enrollment=enrollment)
            for choice_id in selected_ids:
                try:
                    choice = Choice.objects.get(pk=choice_id)
                    submission.choices.add(choice)
                except Choice.DoesNotExist:
                    pass
            submission.save()
        return HttpResponseRedirect(reverse('onlinecourse:exam_result', args=(course.id,)))

def show_exam_result(request, course_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        submission = Submission.objects.filter(enrollment=enrollment).last() if enrollment else None
    else:
        submission = None
    
    context['course'] = course
    context['submission'] = submission
    
    selected_choices = submission.choices.all() if submission else []
    score = 0
    for choice in selected_choices:
        if choice.is_correct:
            score += 1
            
    context['score'] = score
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)