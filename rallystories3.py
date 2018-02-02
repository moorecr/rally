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


slack = Slacker('enter slack token here')

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
channel = "#slack channel here"


#cmoore-hackathon-moes
apikey="rally key"




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
    
    Hierarchfields = "FormattedID,Name,Iteration,TaskRemainingTotal,TaskStatus" #,Feature"
    Artifactfields = "owner,tags"

    #criterion = '((Iteration.Name contains "Iteration 3")OR(Iteration.Name contains "Iteration 7")) AND (Feature != null)'
    #query = "%s "
    criterion = '(Iteration.Name contains "PI%s - Iteration %s")' % (pivalue,iterationvalue)
    response = rally.get('HierarchicalRequirement', fetch=Hierarchfields, query=criterion, order="FormattedID",
                                   pagesize=200, limit=400)

  #  artifactresponse = rally.get('Artifacts', fetch=True, query=criterion, order="owner", limit=400)
    print criterion


    postmessage = "*Current Stories Iteration Stories*"+"\n"+"```";
    for story in response:
        
            #print (story.FormattedID,story.Iteration)
            postmessage = postmessage + "%-8s %-70s %-4.1f %-25s" % (story.FormattedID, story.Name,story.TaskRemainingTotal,story.TaskStatus) + "\n"
            taskquery = story.FormattedID
            print taskquery
            taskfields    = "FormattedID,State,Name"
            responsetask = rally.get('Task', fetch=taskfields, query=taskquery, order="FormattedID",
                                   pagesize=200, limit=400)

            for task in responsetask:

                print "%s  %s  %s" % (task.FormattedID, task.Name, task.State)  + "\n"


    postmessage = postmessage + "```" +"\n";
    print response.resultCount, "qualifying stories"
    print postmessage
    #slack.chat.post_message(channel=channel, text=postmessage, username="Rally Story Bot", as_user=False)

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

