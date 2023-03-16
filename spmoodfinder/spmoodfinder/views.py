import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import CacheHandler, CacheFileHandler
from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from frontend import views as frontendviews


client_id = "6619410f74d84543b61f09853f7259cb"
client_secret = "79a0c90081ac46029087c91521d7fa30"
token_info = "token_info"
def home(request):
    global sp_oauth
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url() #AUTHORIZE/
    return redirect(auth_url)
def userDataView(request):
    result_string = ""
    token_info = get_token(request)
    token = token_info['access_token']
    #print("Access Token",token)
    sp = spotipy.Spotify(auth=token)
    user_name = str(sp.current_user()['display_name'])
    # results = sp.current_user_playlists()
    # for i, item in enumerate(results['items']):
    #     if(i != 15):
    #         print(i, item['name'])
    #         result_string += item['name']+"<br>"
    context = {
        'sp': sp
    }
    return frontendviews.mostPlayedView(request,context)

def get_token(request):
    token_info = request.session.get('token_info')
    return token_info

def redirectView(request):
    #SECOND CALL TO GET ACCESS TOKEN
    code = request.GET.get('code')
    #print(code)
    token_info = sp_oauth.get_access_token(code,check_cache=False)
    request.session["token_info"] = token_info 
    #print(token_info)
    response = redirect("http://127.0.0.1:8000/userdata")
    return response
##create spotify OAuth
def create_spotify_oauth(request):
    redirect_url = request.build_absolute_uri() + str("redirect")
    return SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_url,
        scope = "user-top-read user-read-email user-read-private user-read-currently-playing"
    )
def logoutView(request):
    return HttpResponse("you have logged out")
def logout(request):
    for key in list(request.session.keys()):
        request.session.pop(key)
    #print(request.session)
    request.session.flush()
    return redirect('http://accounts.spotify.com/logout')