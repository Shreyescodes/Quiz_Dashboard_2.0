import random
import csv
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm, QuizTypeForm, QuizQuestionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import QuizType, QuizRequest, QuizAttempt, QuizFile, QuizAccess, QuizQuestion
from .forms import SignUpForm, LoginForm, UploadFileForm
from io import StringIO

# Global variable to hold quiz data
quiz_data = []

def upload_file(request):
    global quiz_data
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            quiz_file = form.save(commit=False)
            quiz_file.uploaded_by = request.user
            
            quiz_type_name = form.cleaned_data['quiz_type_name']
            quiz_type, created = QuizType.objects.get_or_create(name=quiz_type_name)
            quiz_file.quiz_type = quiz_type
            quiz_file.is_active = True
            quiz_file.save()
            
            messages.success(request, f"File uploaded successfully for quiz type: {quiz_type.name}")
            return redirect('quiz:admin_dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'quiz/upload.html', {'form': form})

def quiz_types(request):
    types = set((row.get('T_ID'), row.get('Type')) for row in quiz_data)
    return render(request, 'quiz/quiz_types.html', {'types': types})

@login_required
def display_quiz(request, quiz_type_id, quiz_type_name):
    quiz_file = QuizFile.objects.filter(quiz_type_id=quiz_type_id, is_active=True).first()
    if not quiz_file:
        return render(request, 'quiz/no_questions.html')

    # Read the CSV file content
    file_content = quiz_file.file.read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(file_content))
    questions = list(csv_reader)

    # Check if there are any questions for the quiz type and T_ID
    if not questions:
        return render(request, 'quiz/no_questions.html')

    # Reset the quiz if the session data is inconsistent
    if ('shuffled_indices' not in request.session or
        len(request.session['shuffled_indices']) != len(questions) or
        request.session.get('question_index', 0) >= len(questions)):
        request.session['shuffled_indices'] = list(range(len(questions)))
        random.shuffle(request.session['shuffled_indices'])
        request.session['question_index'] = 0
        request.session['score'] = 0
        request.session['incorrect_questions'] = []

    shuffled_indices = request.session['shuffled_indices']
    question_index = request.session['question_index']

    # Check if it's the last question
    is_last_question = (question_index == len(questions) - 1)

    if request.method == 'POST':
        # Handle answer submission
        selected_answer = request.POST.get('answer')

        if not selected_answer:
            messages.error(request, "Please select an option before proceeding.")
        else:
            current_question_index = shuffled_indices[question_index]
            if selected_answer == questions[current_question_index]['Correct answer']:
                request.session['score'] = request.session.get('score', 0) + 1
            else:
                incorrect_questions = request.session.get('incorrect_questions', [])
                incorrect_questions.append({
                    'question': questions[current_question_index]['Questions'],
                    'correct_answer': questions[current_question_index]['Correct answer'],
                    'user_answer': selected_answer
                })
                request.session['incorrect_questions'] = incorrect_questions

            if not is_last_question:
                request.session['question_index'] = question_index + 1
            else:
                # Show the score
                score = request.session.get('score', 0)
                total_questions = len(questions)
                percentage = (score / total_questions) * 100 if total_questions > 0 else 0

                incorrect_questions = request.session.get('incorrect_questions', [])

                # Clear session variables
                for key in ['score', 'question_index', 'incorrect_questions', 'shuffled_indices']:
                    request.session.pop(key, None)

                return render(request, 'quiz/score.html', {
                    'score': score,
                    'total': total_questions,
                    'percentage': percentage,
                    'incorrect_questions': incorrect_questions
                })

            return redirect('quiz:display_quiz', quiz_type_id=quiz_type_id, quiz_type_name=quiz_type_name)

    # Render the current question
    current_question_index = shuffled_indices[question_index]
    
    return render(request, 'quiz/quiz.html', {
        'question': f"{question_index + 1}. {questions[current_question_index]['Questions']}",
        'options': [
            questions[current_question_index]['Option1'],
            questions[current_question_index]['Option2'],
            questions[current_question_index]['Option3'],
            questions[current_question_index]['Option4']
        ],
        'is_last_question': is_last_question,
        'total_questions': len(questions),
        'current_question_number': question_index + 1,
        'quiz_type': quiz_type_name,
    })
    
def quiz_detail(request, question_type):
    questions = QuizQuestion.objects.filter(question_type=question_type)
    return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_type': question_type})

def quiz_types(request):
    types = [
        (1, 'Python'),
        (2, 'Java'),
        (3, 'Javascript')
        # Add other types as needed
    ]
    return render(request, 'quiz/quiz_types.html', {'types': types})

@login_required
def user_dashboard(request):
    active_quiz_types = QuizType.objects.filter(files__is_active=True).distinct()
    pending_requests = QuizAccess.objects.filter(user=request.user, status='pending')
    approved_quizzes = QuizAccess.objects.filter(user=request.user, status='approved')

    # Get quiz types that the user hasn't requested or been approved for
    available_quiz_types = active_quiz_types.exclude(
        id__in=pending_requests.values_list('quiz_type__id', flat=True)
    ).exclude(
        id__in=approved_quizzes.values_list('quiz_type__id', flat=True)
    )

    return render(request, 'quiz/user_dashboard.html', {
        'available_quiz_types': available_quiz_types,
        'pending_requests': pending_requests,
        'approved_quizzes': approved_quizzes,
    })

@login_required
def request_quiz_access(request, quiz_type_id):
    quiz_type = get_object_or_404(QuizType, id=quiz_type_id)
    access, created = QuizAccess.objects.get_or_create(
        user=request.user,
        quiz_type=quiz_type,
        defaults={'status': 'pending'}
    )
    if created:
        messages.success(request, f"Access requested for {quiz_type.name}")
    else:
        messages.info(request, f"Access for {quiz_type.name} was already requested")
    return redirect('quiz:user_dashboard')

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    pending_requests = QuizAccess.objects.filter(status='pending')
    quiz_files = QuizFile.objects.all().order_by('-upload_date')
    return render(request, 'quiz/admin_dashboard.html', {
        'pending_requests': pending_requests,
        'quiz_files': quiz_files,
    })

@user_passes_test(is_admin)
def manage_quiz_access(request, access_id):
    access = get_object_or_404(QuizAccess, id=access_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            access.status = 'approved'
            messages.success(request, f"Access approved for {access.user.username} to {access.quiz_type.name}")
        elif action == 'deny':
            access.status = 'denied'
            messages.success(request, f"Access denied for {access.user.username} to {access.quiz_type.name}")
        access.save()
    return redirect('quiz:admin_dashboard')

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:user_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'quiz/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('quiz:admin_dashboard')
                else:
                    return redirect('quiz:user_dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'quiz/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import QuizType, QuizAccess, QuizFile

@login_required
def user_dashboard(request):
    active_quiz_types = QuizType.objects.filter(files__is_active=True).distinct()
    pending_requests = QuizAccess.objects.filter(user=request.user, status='pending')
    approved_quizzes = QuizAccess.objects.filter(user=request.user, status='approved')

    # Get quiz types that the user hasn't requested or been approved for
    available_quiz_types = active_quiz_types.exclude(
        id__in=pending_requests.values_list('quiz_type__id', flat=True)
    ).exclude(
        id__in=approved_quizzes.values_list('quiz_type__id', flat=True)
    )

    return render(request, 'quiz/user_dashboard.html', {
        'available_quiz_types': available_quiz_types,
        'pending_requests': pending_requests,
        'approved_quizzes': approved_quizzes,
    })

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('quiz:login')