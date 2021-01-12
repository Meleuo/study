from django.shortcuts import render
import time

# Create your views here.
def test_view(request):
    return render(request, 'test.html', {
        'time': time.time()
    })
