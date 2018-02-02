
#!/usr/bin/env python

#################################################################################################
#
#  showstories -- show stories in a workspace/project conforming to some common criterion
#  using a Rally WS API query syntax mixing AND and OR operators
#
#################################################################################################




import sys, os
import argparse
from pyral import Rally, rallyWorkset, RallyRESTAPIError
from slacker import Slacker


slack = Slacker('slack token here')

#################################################################################################

errout = sys.stderr.write

server="rally1.rallydev.com"

#as we are using an API key, we can leave out the username and password
user=""
password=""

# workspace ID for NaviSite
workspace="NaviSite Workspace"
# project ID for Team Systems Team for Systems and Teams
project="Team Systems Team for Systems and Teams"
# API key for tandre 1/13/2017

#slack channel
channel = "#systems_keepout"


#cmoore-hackathon-moes
apikey="rallyapi here"

rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)


usresponse = rally.get('UserStory', fetch=True, query='FormattedID = 1716')
story1 = usresponse.next()
print story1.details()


response = rally.get('Task', fetch=True, query='FormattedID = 2963')
story2 = response.next()
print story2.details()
