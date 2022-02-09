from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from dipreazione import forms
from dipreazione import models

import datetime
import collections

def index(request):
    ctx = { 'form': forms.CreateMeatingForm }
    return render(request, 'dipreazione/index.html', ctx)

def new_meating(request):
    if request.method != 'POST':
        return HttpResponse("sucaa")

    form = forms.CreateMeatingForm(request.POST)
    if not form.is_valid():
        return HttpResponse("VAFANTOCU")

    meating = models.Meating(
        name=form.cleaned_data['name'],
        start_date=datetime.date.today()
    )

    meating.save()

    return HttpResponseRedirect(reverse('meating', args=(meating.id,)))

def meating(request, meating_id):
    meating = get_object_or_404(models.Meating, pk=meating_id)

    potential_dates = [
        meating.start_date + datetime.timedelta(days=i)
            for i in range(15) ]

    preferences = models.Preference.objects.filter(
        meating=meating
    )

    by_meater = collections.defaultdict(dict)
    date_count = collections.Counter()

    for p in preferences:
        by_meater[p.meater][p.date] = True
        date_count[p.date] += 1

    totals = [ date_count[date]
         for date in potential_dates ]

    rows = []

    for meater, prefs in by_meater.items():
        row = []
        rows.append({'meater': meater.name, 'p': row})

        for date in potential_dates:
            row.append(prefs.get(date, False))

    c = {
        'meating': meating,
        'potential_dates': potential_dates,
        'totals': totals,
        'rows': rows,
        'histogram': date_count.most_common(),
    }

    return render(request, 'dipreazione/meating.html', c)

def submit_meating(request, meating_id):
    meating = get_object_or_404(models.Meating, pk=meating_id)
    
    meater, _ = models.Meater.objects.get_or_create(
        name=request.POST['meater']
    )

    old_prefs = models.Preference.objects.filter(
        meating=meating,
        meater=meater
    )

    old_prefs.delete()  # allow re-posting same name different dates

    pref_dates = request.POST.getlist('dates')
    
    pref_dates = [
        datetime.datetime.strptime(d, '%d%m%Y').date()
            for d in pref_dates]

    for date in pref_dates:
        pref = models.Preference(
            meating=meating,
            meater=meater,
            date=date
        )

        pref.save()

    return HttpResponseRedirect(reverse('meating', args=(meating.id,)))
