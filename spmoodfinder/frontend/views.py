from django.shortcuts import render

def mostPlayedView(request,context):
    sp = context['sp']
    songplayingnow = sp.current_user_playing_track()
    data = {
        "songname" : songplayingnow['item']['artists'][0]['name']
    }
    return render(request,'frontend/index.html',data)
