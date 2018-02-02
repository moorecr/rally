#!/usr/bin/env python

#################################################################################################
#
#  showstories -- show stories in a workspace/project conforming to some common criterion
#  using a Rally WS API query syntax mixing AND and OR operators
#
#################################################################################################




import sys, os
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
channel = "#a-team"


#cmoore-hackathon-moes
apikey="_2yrazrNvTmOYVUDC1GqvF9aKnpSsUsgrgrQaxN50Y"

#################################################################################################

def main(args):
    options = [opt for opt in args if opt.startswith('--')]
    args    = [arg for arg in args if arg not in options]
    #server, user, password, apikey, workspace, project = rallyWorkset(options)
    #if apikey:
    rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)
    #else:
    #    rally = Rally(server, user, password, workspace=workspace, project=project)
    rally.enableLogging("rally.history.showstories")
    
    Hierarchfields    = "FormattedID,Name,Iteration,TaskRemainingTotal,TaskStatus" #,Feature"
    
    #criterion = '((Iteration.Name contains "Iteration 3")OR(Iteration.Name contains "Iteration 7")) AND (Feature != null)'
    criterion = '(Iteration.Name contains "PI3 - Iteration 3")'
    response = rally.get('HierarchicalRequirement', fetch=Hierarchfields, query=criterion, order="FormattedID",
                                   pagesize=200, limit=400)

    postmessage = "*Current Stories Iteration Stories*"+"\n"+"```";
    for story in response:
        #print (story.FormattedID,story.Iteration)
        postmessage = postmessage + "%-8s %-70s %-4.1f %-25s" % (story.FormattedID, story.Name,story.TaskRemainingTotal,story.TaskStatus) + "\n";

    postmessage = postmessage + "-----------------------------------------------------------------```" +"\n";
    print response.resultCount, "qualifying stories"

    slack.chat.post_message(channel=channel, text=postmessage, username="rallyslackbot", as_user=False)

#################################################################################################
#################################################################################################

if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)

