from django.shortcuts import render
import lyricsgenius

def mostPlayedView(request,context):
    sp = context['sp']
    songplayingnow = sp.current_user_playing_track()
    
    id = songplayingnow['item']['id'] 
    analysis = sp.audio_analysis(id)

    genius = lyricsgenius.Genius("qilNVtKPjI7QgAsc9LPJjxdyyGk-G7k3b-XC9tIUGgi8tJZlJ0S_hAH3CbbB4SWe",timeout=120)
    artist_name = songplayingnow['item']['artists'][0]['name']
    #artist = genius.search_artist(, max_songs=100, sort="title")
    song_name= songplayingnow['item']['name']
    song = genius.search_song(song_name,artist_name)
    lyrics_data = song.lyrics
    #formatted_song = genius.song_annotations(song.id,text_format ='html')
    #print("\n\n##############\n\n{}\n\n#################\n\n".format(formatted_song))
    lyrics = lyrics_data.split('\n')
    print(lyrics)
    display_lyrics = []
    for ele in lyrics[0:]:
    
        print(ele)
        display_lyrics.append(ele)
        #lyrics.append(ele)

        
    try:
        
        data = {
            "songname" : songplayingnow['item']['name'],
            "songimage": songplayingnow['item']['album']['images'][0]['url'],
            "analysis" : analysis,
            "lyrics"   : display_lyrics
        }
    except TypeError:
        data = {
            "songname" : "Nothing is Playing"
        }
    return render(request,'frontend/index.html',data)
