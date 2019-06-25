import requests
import os
import sys
import json
import spotipy
import spotipy.util as util
from django.shortcuts import render
import webbrowser
from .models import Artist
from .forms import ArtistForm
import urllib3
from json.decoder import JSONDecodeError


# Create your views here.


def index(request):
    #TODO get artists info at spotify from concert informations.

    target_name = 'spotify'

    user_name = "i581c4m3ajdm2a2s8zcon0yr6"

    client_id = "126830b6c4ea48f781e1cc6e11e355e0"
    client_secret = "d6b0c8be0bbf4b0b8d5b97c3cdad6c40"
    redirect_uri = 'http://www.google.ca'  # dont use same page url as redirect uri.

    scopes = 'user-library-read user-read-recently-played'

    def check_duplicated_name(name):
        arts = Artist.objects.all()
        artist_pool = []
        for art in arts:
            artist_pool.append(art.__str__())
        if name in artist_pool:
            return False
        else:
            return True

    # Post name may not equal to returned name. its buggy.
    if request.method == 'POST':
        if check_duplicated_name(request.POST['name']):
            form = ArtistForm(request.POST)
            form.save()
        else:
            print("name duplicated")
    form = ArtistForm()

    def decode_chinese_name():
        chinese_tester = "邓紫棋"
        encoded_string = chinese_tester.encode('utf-8')
        print(str(encoded_string)[2:-1].replace("\\x", "%").upper())

    artists = Artist.objects.all()

    token = util.prompt_for_user_token(user_name, client_id=client_id, client_secret=client_secret,
                                       redirect_uri=redirect_uri, scope=scopes)
    sp = spotipy.Spotify(auth=token)

    user = sp.current_user()
    user_recently_played = sp.current_user_saved_albums(limit=1, offset=0)
    display_name = user['display_name']

    with open('Files/SavedAlbum', 'w') as outfile:
        for ele in user_recently_played:
            json.dump(ele, outfile, separators=(',', ':'))
            outfile.write('\n')
        outfile.close()

    artists_data = []
    for artist in artists:
        art_str = artist.__str__()
        results = sp.search(q='artist:' + art_str, type='artist')
        items = results['artists']['items']
        follower = items[0]['followers']['total']
        artist_name = None
        artist_genre = None
        if len(items) > 0:
            _artist = items[0]

            artist_name = _artist['name']
            artist_genre = _artist['genres'][0]

            # webbrowser.open(_artist['images'][0]['url'])
        print(artist_genre)
        artist_context = {
            'main_name': target_name,
            'display_name': display_name,
            'follower': follower,
            'artist_name': artist_name,
            'artist_genre': artist_genre
        }

        artists_data.append(artist_context)

    context = {"artists_data": artists_data, "form": form}
    return render(request, 'Basic.html', context)
