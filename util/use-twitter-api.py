import twitter
import pprint

consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
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
