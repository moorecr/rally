#note, you'll need to be running python2 (built with 2.7, python DOES NOT WORK )
#you'll need to pip install pyral (the python-rally connector) as slacker (the slack connector)
#    sudo pip install slacker

# source: MartinCron https://github.com/MartinCron/rally_slack_integration/blob/master/rallyslack.py#L1
#  


from datetime import datetime
from datetime import timedelta
from pyral import Rally
from slacker import Slacker

slack = Slacker('enter slack token here')

# Send a message to #integration-testing channel

server="rally1.rallydev.com"

#as we are using an API key, we can leave out the username and password
user=""
password=""

# workspace ID for NaviSite
workspace="NaviSite Workspace"
# project ID for Team Systems Team for Systems and Teams
project="Team Systems Team for Systems and Teams"
# API key for tandre 1/13/2017

#cmoore-hackathon-moes

apikey="rally api key here"

#which slack channel does this post to?
channel = "#channel name here"

#Assume this system runs (via cron) every 15 minutes.
interval = 1000 * 60

#format of the date strings as we get them from rally
format = "%Y-%m-%dT%H:%M:%S.%fZ"

#create the rally service wrapper
rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)


#build the query to get only the artifacts (user stories and defects) updated in the last day
querydelta = timedelta(days=-1)
querystartdate = datetime.utcnow() + querydelta;
query = 'LastUpdateDate > ' + querystartdate.isoformat()

response = rally.get('Artifact', fetch=True, query=query, order='LastUpdateDate desc')
for artifact in response:
	include = False

	#start building the message string that may or may not be sent up to slack
	postmessage = '*' + artifact.FormattedID + '*'
	postmessage = postmessage + ': ' + artifact.Name + '\n';
	for revision in artifact.RevisionHistory.Revisions: 
		revisionDate = datetime.strptime(revision.CreationDate, format)
		age = revisionDate - datetime.utcnow()
		seconds = abs(age.total_seconds())
		#only even consider this story for inclusion if the timestamp on the revision is less than iterval seconds onld

		if seconds < interval:
			description = revision.Description
			items = description.split(',')
			task =  

			for item in items:
				item = item.strip()
				#the only kinds of updates we care about are changes to OWNER and SCHEDULE STATE
				#other changes, such as moving ranks around, etc, don't matter so much
				if item.startswith('SCHEDULE STATE ') or item.startswith("OWNER added "):
					postmessage = postmessage  + "> " + item + ' \n';

								
					include = True

	
	if include:
		postmessage = postmessage + 'https://rally1.rallydev.com/#/search?keywords=' + artifact.FormattedID + '\n'
		#slack.chat.post_message(channel=channel, text=postmessage, username="rallyslackbot", as_user=False)
        print postmessage
