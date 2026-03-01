from django.shortcuts import render, redirect
from .models import Feedback
from .forms import FeedbackForm

def home(request):
    return render(request, 'home.html')

def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_feedback')
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})

def all_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'all_feedback.html', {'feedbacks': feedbacks})
