from flask import Flask, render_template, request

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from urllib.parse import urlencode
import json
from protorpc.messages import StringField
import argparse
import tmdbsimple as tmdb

app = Flask(__name__)

app.debug=True

@app.route('/hello', methods=['POST', 'GET'])
def helloWorld():

  mysearch = "bunnies in cups"
  if request.method == 'POST':
    rawsearch = request.form['searchstr']
    mysearch = rawsearch + " trailer"
    

  argparser = argparse.ArgumentParser()
  print(mysearch)
  argparser.add_argument("--q", help="Search term", default=mysearch)
  argparser.add_argument("--max-results", help="Max results", default=10)
  args = argparser.parse_args()
  

  title = "bunnies in cups"
  overview = ""

  if request.method == 'POST':
    s = tmdb.Search()
    r = s.movie(query=str(rawsearch))
  
    print(s.results)
    if len(s.results) > 0:
      title = s.results[0]['title']
      overview = s.results[0]['overview']
  
  name = "Connor and Zach's Mashup"
  try:
    mysearchreturn = youtube_search(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

  if request.method == 'POST':
    if mysearchreturn == False or len(s.results) == 0:
      return render_template('basic.html', name=name, myvidid=json.dumps(mysearchreturn), myheight='320', title=title, overview=overview)

  return render_template('hello.html', name=name, myvidid=json.dumps(mysearchreturn), myheight='320', title=title, overview=overview)



DEVELOPER_KEY = "AIzaSyB4nLV_JF3ieTxWdJLMRhdlOqPedvrfavc"
tmdb.API_KEY = '5104f9dd4c2020b42f6cadc29e5b6d23'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  #print(search_response.get("items", [])[1])

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  myvid = None
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      if myvid == None:
        myvid = search_result["id"]["videoId"]
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
  if myvid != None:
    return myvid
  else:
    return False
      

  print("Videos:\n", "\n".join(videos), "\n")
  #print("Channels:\n", "\n".join(channels), "\n")
  #print("Playlists:\n", "\n".join(playlists), "\n")


if __name__ == "__main__":
  app.run()