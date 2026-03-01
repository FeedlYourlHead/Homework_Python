from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm

def home(request):
    return render(request, 'feedback/home.html')

def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваш отзыв')
            return redirect('all_feedback')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})

@login_required
def all_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/all_feedback.html', {'feedbacks': feedbacks})
