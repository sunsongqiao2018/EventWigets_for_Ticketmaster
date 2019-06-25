import requests
import os
import sys
import json
import spotipy
import spotipy.util as util
from django.shortcuts import render
import webbrowser
import urllib3
from .forms import SizeForm, EventForm
from .models import Event
from json.decoder import JSONDecodeError
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def index(request):

    tm_key = '1vpxAmJjnqIidqU1szoLZvXlxp2TBmnB'
    tm_secret = 'bSyTMkK0ms7nLSot'
    tm_root_url = "https://app.ticketmaster.com/"
    # template tm_uri: https://app.ticketmaster.com/{package}/{version}/{resource}.json?apikey=**{API key}
    tm_packages = ["discovery", "partner", "top-picks", "inventory-status", "mfxapi", "presence"]
    tm_country_code = ['CA', 'US']
    tm_classfication_name = 'music'
    event_model = Event
    #clean every model in previous search
    event_model.objects.all().delete()
    events_data=[]
    if request.method == 'POST':
        event_size_form = SizeForm(request.POST)

        if event_size_form.is_valid():

            event_size = event_size_form.cleaned_data['event_size']

            r = requests.get(f"https://app.ticketmaster.com/{tm_packages[0]}/v2/events.json?size={event_size}&countryCode=CA&classificationName='music'&apikey={tm_key}")

            event_json = r.json()
            parsed_event = event_json["_embedded"]["events"]

            # extract one sample event to local file
            with open('Files/SavedEvent.json', 'w') as outfile:
                json.dump(parsed_event[0], outfile, indent=4)
                outfile.close()

            item_url = None
            if parsed_event.__len__() > 0:
                for n in range(0, parsed_event.__len__()):
                    event_id = parsed_event[n]['id']
                    event_name = parsed_event[n]['name']
                    event_url = parsed_event[n]['url']
                    first_item = parsed_event[n]['images']
                    for img in first_item:
                        if img["width"] == 640 and img['height'] == 360:
                            item_url = img['url']

                    event_context = {
                        "event_id": event_id,
                        "img_url": item_url,
                        'event_name': event_name,
                        'event_url': event_url,
                    }
                    events_data.append(event_context)

                    new_event = Event(event_id=event_id, name=event_name, event_url=event_url, img_url=item_url)
                    new_event.save()
                    # put queryEvent into database:
            for event in Event.objects.values_list('event_id', flat=True).distinct():
                Event.objects.filter(pk__in=Event.objects.filter(event_id=event_id)
                                     .values_list('event_id', flat=True)[1:]).delete()
    else:
        # Create empty form for user
        event_size_form = SizeForm()

    context = {'events_data': events_data, 'size_form': event_size_form}
    return render(request, 'EventSearch.html', context)

# view for event detail widgets


def eventdetail(request, event_id):
    event_model = Event
    event_info = event_model.objects.get(event_id=event_id)

    event_img = event_info.img_url
    event_name = event_info.name
    event_url = event_info.event_url

    context = {
        'event_name': event_name,
        'event_url': event_url,
        'img_url': event_img
    }
    return render(request, 'EventWidget.html', context)
