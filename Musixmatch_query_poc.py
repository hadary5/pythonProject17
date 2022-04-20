import csv
import requests
from musixmatch import Musixmatch,utils
from datetime import datetime
import configuration

api_key=configuration.KEY
musixmatch = Musixmatch(api_key)
default_search_word='car'
default_album_search_date=datetime.strptime('2010-1-1', '%Y-%m-%d')

def musixmatch_search_lyrics(q_lyrics=default_search_word):
    url_base = 'http://api.musixmatch.com/ws/1.1/'
    url='track.search?q_lyrics='+q_lyrics
    url=url+'&page_size='+str(utils._set_page_size(10))
    url=url+'&page='+str(1)
    url=url+'&s_track_rating='+'desc'
    url=url+'&f_lyrics_language=en'
    full_url=url_base + '{}&apikey={}'.format(url, api_key)
    data = requests.get(full_url).json()
    return data
if __name__ == "__main__":
    #search_lyrics_acording_keyword=musixmatch.track_search("1","a" ,page_size=10, page=1,s_track_rating='desc')
    search_result_lyrics_acording_to_keyword=musixmatch_search_lyrics("boom")

    #print(search_result_lyrics_acording_to_keyword['message']['body']['track_list'][0])

    save_songs_details_list=[]
    #go over the results
    #songs from albums prior to album search date will be save
    #with the flowing attributes
    #song_name,performer_name,album_name,song share url
    for track_item in search_result_lyrics_acording_to_keyword['message']['body']['track_list']:
        current_song_dict={}
        a_valid_date_format=True
        #print(track_item['track']['album_id'])
        current_album_id=track_item['track']['album_id']
        current_album_data=musixmatch.album_get(current_album_id)
        print(current_album_data['message']['body']['album']['album_release_date'])
        curent_album_date=current_album_data['message']['body']['album']['album_release_date']
        try:
            curent_album_date= datetime.strptime(curent_album_date, '%Y-%m-%d')
        except(ValueError):
            try:
                curent_album_date = datetime.strptime(curent_album_date, '%Y')
            except(ValueError):
                a_valid_date_format=False

        #print(curent_album_date)
        if a_valid_date_format and curent_album_date < default_album_search_date:
            print("this one:\n",track_item['track'])
            current_song_dict['song_name']=track_item['track']['track_name']
            current_song_dict['performer_name']=track_item['track']['artist_name']
            current_song_dict['album_name'] = track_item['track']['album_name']
            current_song_dict['song_share_url']=track_item['track']['track_share_url']
            save_songs_details_list.append(current_song_dict)
    print(save_songs_details_list)
    if save_songs_details_list:
        keys = save_songs_details_list[0].keys()
        with open('test.csv', 'a') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=',')
            dict_writer.writeheader()
            dict_writer.writerows(save_songs_details_list)
