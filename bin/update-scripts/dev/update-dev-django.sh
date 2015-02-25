#!/bin/bash
#
# This must match the name of the webapp in the Chief configs (/var/www/chief/settings.py)
# This should be the only change you need to make.
WEBAPP="bedrock.dev"

function checkretval(){
    retval=$?
    if [[ $retval -gt 0 ]]; then
        echo "Error!!! Exit status of the last command was $retval"
        exit $retval
    fi
}

# Get the sha currently deployed
SHADEPLOYED=$(curl -s -XGET https://www-dev.allizom.org/media/revision.txt)
SHAAVAILABLE=$(git ls-remote git://github.com/mozilla/bedrock.git master | awk '{print $1;}')
# Nix the 4 bytes before the sha because it's http smart protocol
#SHAAVAILABLE="${SHAAVAILABLE:4}"

echo "We have ${SHADEPLOYED:0:8} and ${SHAAVAILABLE:0:8} is available."

if [ "$SHADEPLOYED" = "$SHAAVAILABLE" ];
then
    # Nothing to deploy
    echo "Nothing to deploy."
    exit 0
fi

# Here we will load the WEBAPPS object from the Chief configs and grab the update password for our $WEBAPP
PASSWORD=$(/data/bedrock-dev/src/www-dev.allizom.org-django/password.py)

# If there was an error in the python we will raise it here ($PASSWORD contains the error in this case)
if [ $? != 0 ]; then
    echo -e "$PASSWORD"
    exit 1
fi

echo "Calling Chief for '$WEBAPP' to deploy '${SHAAVAILABLE:0:8}'"

# This just creates a POST event to the Chief app. We populate the form fields with the information gathered above ($SHAAVAILABLE, $PASSWORD, $WEBAPP)
curl -s -F 'who=web-ops_cli_script' -F "password=$PASSWORD" -F "ref=$SHAAVAILABLE" http://$(hostname)/chief/$WEBAPP -o /dev/null
checkretval

