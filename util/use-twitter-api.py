import twitter
import pprint

consumer_key = 'sJoKW3WVonOYoHPh4yEEwLBgv'
consumer_secret = 'm82kjSEBQNXfiX17ABsFa1QkqnKZW04Na4qONVeHurjwGDUTv2'
access_token_key = '7686862-dImzWYT4fRvGl8wPpJO6mfBNliZZEcUTMCdoM1fZq7'
access_token_secret = 'zihJwRrEBeQh7vaUC77zSfoAb0R74Ov4P8KGRQX2DsfEM'
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)
print "Verify Credentials"
pprint.pprint(api.VerifyCredentials())

list_members = api.GetListMembers(None, 'ord-campers', owner_screen_name='therealfitz')
print "\nlist members: {}".format(len(list_members))

print "\nfirst member"
print list_members[0].screen_name
print list_members[0].name
print list_members[0].profile_image_url
pprint.pprint(list_members[0].AsDict())
