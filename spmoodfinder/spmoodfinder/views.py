import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import render,redirect
from django.http import HttpResponse

client_id = "6619410f74d84543b61f09853f7259cb"
client_secret = "79a0c90081ac46029087c91521d7fa30"
token_info = "token_info"

def home(request):
    global sp_oauth
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
    
    # return redirectView(auth_url) 
    # return HttpResponse("Hello "+str(request.build_absolute_uri()))

def getTracksView(request):

    response_string = str()
    token_info = get_token(request)
    print("\n\nTHIS IS THE ACCESS TOKEN:\n#######################\n",token_info['access_token']+"\n\n")
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)
    for sp_range in ['short_term', 'medium_term', 'long_term']:
        print("range:", sp_range)
        results = sp.current_user_top_artists(time_range=sp_range, limit=50)
        for i, item in enumerate(results['items']):
            response_string += item['name']+"<br>"
            print(i,item['name'])
    return HttpResponse("<h1>{}</h1>".format(response_string))

def get_token(request):
    token_info = request.session.get('token_info')
    return token_info

def redirectView(request):
    request.session.flush()
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session["token_info"] = token_info

    response = redirect("http://127.0.0.1:8000/getTracks")
    return response
    

def create_spotify_oauth(request):
    redirect_url = request.build_absolute_uri() + str("redirect")
    return SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_url,
        scope = "user-library-read user-top-read"
    )

def logoutView(request):
    return HttpResponse("you have logged out")
# def logout(request):
#     request.session['token_info'] = "{ }"
#     # token_info = get_token(request)
#     # print("\n\nTHIS IS THE ACCESS TOKEN FROM LOGOUT:\n#######################\n",token_info+"\n\n")
#     response = redirect("http://accounts.spotify.com/logout")
#     #response1 = redirect("http://127.0.0.1:8000/")
#     return response
def logout(request):
    for key in list(request.session.keys()):
        request.session.pop(key)
    print(request.session)
    return redirect('/logoutView')