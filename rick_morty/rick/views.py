from django.shortcuts import render
from rick.models import Cards
def cards(request):
    cards = Cards.objects.all()
    return render(request, 'index.html', {'cards': cards})
