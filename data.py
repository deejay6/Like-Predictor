import requests, urllib
from access_token import ACCESS_TOKEN
import csv
BASE_URL = 'https://api.instagram.com/v1/'
user_list = []


def add_user():
    username = raw_input("Enter Username: ")
    with open("data.csv", 'a') as f1:
        writer = csv.DictWriter(f1, fieldnames=['likes', 'followers', 'filter', 'location', 'hashtag'], delimiter=';')
        writer.writeheader()
        request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (username, ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                id = user_info['data'][0]['id']
                request_url1 = (BASE_URL + "users/%s/?access_token=%s") % (id, ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url1)
                user_info1 = requests.get(request_url1).json()
                followers = user_info1['data']['counts']['followed_by']
                print followers
                request_url2 = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (id, ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url2)
                user_media = requests.get(request_url2).json()
                for i in range(0, len(user_media['data'])):
                    filter1 = user_media['data'][i]['filter']
                    likes = user_media['data'][i]['likes']['count']
                    if user_media['data'][i]['location']:
                        location = user_media['data'][i]['location']['name']
                    else:
                        location = None
                    if len(user_media['data'][i]['tags']):
                        for j in range(0 , len(user_media['data'][i]['tags'])):
                            hashtag = user_media['data'][i]['tags'][j]
                            try:
                                writer.writerow({'likes': likes, 'followers': followers, 'filter': filter1, 'location': location,
                                                 'hashtag': hashtag})
                            except:
                                continue
                    else:
                        hashtag = None
                        writer.writerow({'likes': likes, 'followers': followers, 'filter': filter1, 'location': location,
                                         'hashtag': hashtag})
            else:
                print "Invalid username!!"
        else:
            print "Status code not 200!"


add_user()