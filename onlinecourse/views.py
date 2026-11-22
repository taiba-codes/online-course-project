from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Check if the user is authenticated and enrolled
    if request.method == 'POST':
        # Get selected choices from the form POST request
        choices_ids = request.POST.getlist('choice')
        
        # Get or create enrollment for the current user and course
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )
        
        # Create a new submission object
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Add selected choices to the submission
        for choice_id in choices_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
            
        submission.save()
        
        # Redirect to the exam result view with submission id
        return redirect(reverse('onlinecourse:show_exam_result', args={course.id, submission.id}))
    
    return redirect('onlinecourse:course_details', course_id=course.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate total score based on correct choices selected in submission
    score = 0
    total_score = 0
    
    # Assuming questions have grades and choices are checked
    questions = Question.objects.filter(lesson__course=course)
    for question in questions:
        total_score += question.grade
        # Check if user selected the correct choice for this question
        user_choices = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)
        
        # If user choices match correct choices precisely or partially based on logic
        user_choice_ids = set(user_choices.values_list('id', flat=True))
        correct_choice_ids = set(correct_choices.values_list('id', flat=True))
        
        if user_choice_ids == correct_choice_ids:
            score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': score,
        'total_score': total_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)