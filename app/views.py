from django.utils import timezone
from django.shortcuts import render

# Create your views here.
def main(request):
    context = {
        'timestamp': timezone.now()
    }
    return render(request, 'main.html', context)