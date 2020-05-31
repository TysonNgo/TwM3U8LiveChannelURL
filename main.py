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

access = requests.get(
	'https://api.twitch.tv/api/channels/'+channel_name+
	'/access_token'+
	'?oauth_token=undefined'+
	'&need_https=true'+
	'&platform=_'+
	'&player_type=site'+
	'&player_backend=mediaplayer',
	headers=headers).json()

url = (
	'https://usher.ttvnw.net/api/channel/hls/'+channel_name+'.m3u8'+
	'?sig='+access['sig']+
	'&token='+quote(access['token'])
)

print (url)

#a = requests.get(url)
#print (a)
