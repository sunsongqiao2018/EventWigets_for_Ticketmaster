from django.shortcuts import render
import requests
import json
import webbrowser


# Create your views here.


def index(request):
    #TODO get event info with markup prices.
    target_name = 'seatgeek'
    seatgeek_id = 'MTY5MDUwNTd8MTU1OTc1MzEyMC42Mw'
    seatgeek_secret = '9325.......'
    redirect_uri = 'https://www.chumi.co/'
    prime_factor = ['events', 'performers', 'venues']
    second_factor = ''
    url_first_event = ''
    if second_factor is not '':
        url_first_event = f'https://api.seatgeek.com/2/{prime_factor[0]}/{second_factor}?client_id={seatgeek_id}'
    else:
        url_first_event = f'https://api.seatgeek.com/2/{prime_factor[2]}?city=toronto&client_id={seatgeek_id}'

    url = f'https://api.seatgeek.com/2/taxonomies?client_id={seatgeek_id}'

    r = requests.get(url_first_event)
    rjson = r.json()
    if request.method == "GET":
        print(request.GET)
    try:
        consert_num = 49
        # edited_json = rjson["taxonomies"][consertNum]
    except NameError:
        print("not found taxonomies in editedjson")

    webbrowser.open(url_first_event)

    event_title = 'default'
    event_date = 'default'

    # if 'stats' in edited_json:
    #     event_title = edited_json['stats']['performer_count']
    #     event_date = edited_json['stats']['next_event_datetime_utc']

    context = {
        'main_name': target_name,
        'display_name': event_title,
        'follower': event_date,
        'artist_name': second_factor
    }
    return render(request, 'Basic.html', context)
