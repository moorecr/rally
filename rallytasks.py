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


slack = Slacker('xoxp-44257107201-44276984259-128037794102-2db84e9c35494063500fcadaebbe6d0f')

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
apikey="_2yrazrNvTmOYVUDC1GqvF9aKnpSsUsgrgrQaxN50Y"


def main(args):
	options = [opt for opt in args if opt.startswith('--')]
	args    = [arg for arg in args if arg not in options]
	   
	rally = Rally(server, apikey=apikey, workspace=workspace, project=project)
	rally.enableLogging("rally.history.showitems")

	fields    = "FormattedID,State,Name,ToDo"
	    #criterion = 'State != Closed'
	    #taskcriterion = 'iteration = /iteration/20502967321'
	    

	taskcriterion = '(Iteration.Name contains "PI%s - Iteration %s")' % (pivalue,iterationvalue)

	response = rally.get('Task', fetch=fields, query=taskcriterion, order="FormattedID",
	                                   pagesize=200, limit=400)
	postmessage = "*Current Tasks for Iteration*" + "\n";
	for task in response:
			#print
			postmessage = postmessage + "`" + "%-8s %-70s %-4.1f %-25s" % (task.FormattedID, task.Name, task.ToDo, task.State) + "`" + "\n";
#new %-8s %-70s %-4.1f %-25s
#old %-8.8s  %-80.80s  %-10.10s  %-15.15s
	#postmessage = postmessage + "```" + "\n";
	 
	print response.resultCount, "qualifying tasks"
	print postmessage

	slack.chat.post_message(channel=channel, text=postmessage, username="Rally Task Bot", as_user=False)
#################################################################################################
#################################################################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script retrieves schedules from a given server')
    # Add arguments
    parser.add_argument(
        '-P', '--PI', type=int, help='PI number to use in query', required=True)
    parser.add_argument(
        '-I', '--iteration', type=int, help='Iteraton number to use in query', required=True)
    # Array for all arguments passed to script
    args = parser.parse_args()
    pivalue = args.PI
    iterationvalue = args.iteration
    print pivalue, iterationvalue
    main(sys.argv[1:])
    sys.exit(0)
