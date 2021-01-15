import sys

if len(sys.argv) < 2:
	print ('Enter channel name.')
	print ('Example:')
	print ('\tpython main.py channel_name')
	sys.exit()

import requests
import re

try:
	# python 2
	import urllib
	quote = urllib.quote_plus
except:
	# python 3
	import urllib.parse
	quote = urllib.parse.quote

channel_name = sys.argv[1]

def get_client_id():
	html = requests.get('https://www.twitch.tv/'+channel_name).content.decode('utf-8')
	client_id = re.findall('"Client-ID":"(.*?)"', html)
	if client_id:
		return client_id.pop()
	else:
		raise Exception('cannot find Client-ID')

headers = {"client-id": get_client_id()}

"""
access = requests.get(
	'https://api.twitch.tv/v5/channels/'+channel_name+
	'/access_token'+
	'?oauth_token=undefined'+
	'&need_https=true'+
	'&platform=_'+
	'&player_type=site'+
	'&player_backend=mediaplayer',
	headers=headers).json()
"""

data = "{\"operationName\":\"PlaybackAccessToken_Template\",\"query\":\"query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: \\\"web\\\", playerBackend: \\\"mediaplayer\\\", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: \\\"web\\\", playerBackend: \\\"mediaplayer\\\", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}\",\"variables\":{\"isLive\":true,\"login\":\"##CHANNEL_NAME##\",\"isVod\":false,\"vodID\":\"\",\"playerType\":\"site\"}}".replace("##CHANNEL_NAME##", channel_name)
access = requests.post('https://gql.twitch.tv/gql', headers=headers, data=data).json()

signature = access['data']['streamPlaybackAccessToken']['signature']
token = access['data']['streamPlaybackAccessToken']['value']

url = (
	'https://usher.ttvnw.net/api/channel/hls/'+channel_name+'.m3u8'+
	'?sig='+signature+
	'&token='+quote(token)
)

print (url)

#a = requests.get(url)
#print (a)
