#Based on work by Buddy Lindsey (BuddyL) on the Mozilla Kuma project
import json
import urllib
import subprocess
from collections import namedtuple


Human = namedtuple('Human', ['name', 'website'])


def generate_file(target, URLs):

    for repo in URLs:
        if repo['type'] == 'github':
            contributors = get_github(repo['url'])
        elif repo['type'] == 'svn':
            contributors = get_svn(repo['url'])
        else:
            contributors = None
        if contributors:
            write_to_file(contributors, target, repo['header'],
                               repo['prepend'])


def write_to_file(humans, target, message, role):
    target.write("%s \n" % message)
    for h in humans:
        target.write("%s: %s \n" % (role, h.name.encode('ascii',
                                                        'ignore')))
        if(h.website is not None):
            target.write("Website: %s \n" % h.website)
            target.write('\n')
    target.write('\n')


def get_github(url):
    contributors = json.load(urllib.urlopen(url))

    return [Human(contributor.get('name', contributor['login']), contributor.get('website'))
           for contributor in contributors]


def get_svn(url):
    p = subprocess.Popen("svn log --quiet " + url + " | grep '^r' | awk " +
                         "'{print $3}' | sort | uniq",
                         shell=True, stdout=subprocess.PIPE)
    contributors = p.communicate()[0].rstrip().split('\n', -1)

    return [Human(contributor, None) for contributor in contributors]
