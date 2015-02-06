import urlparse
import sys

from django.conf import settings

import MySQLdb

from bedrock.mozorg.models import ContributorActivity


urlparse.uses_netloc.append('mysql')
QUERY = ('SELECT c_date, team_name, source_name, count(*) AS total, IFNULL(SUM(is_new), 0) AS new '
         'FROM contributor_active {where} GROUP BY c_date, team_name, source_name')


def run():
    """Get contributor activity data from Tableau and insert it into bedrock DB."""
    if not settings.TABLEAU_DB_URL:
        print 'Must set TABLEAU_DB_URL.'
        sys.exit(1)

    url = urlparse.urlparse(settings.TABLEAU_DB_URL)
    if not url.path:
        # bad db url
        print 'TABLEAU_DB_URL not parseable.'
        sys.exit(1)

    con_data = {
        # remove slash
        'db': url.path[1:],
        'user': url.username,
        'passwd': url.password,
        'host': url.hostname,
    }
    con = None

    try:
        latest_date = ContributorActivity.objects.only('date').latest().date
        where_clause = 'WHERE c_date > "{0}"'.format(latest_date.isoformat())
    except ContributorActivity.DoesNotExist:
        where_clause = ''

    try:
        con = MySQLdb.connect(**con_data)
        cur = con.cursor()
        cur.execute(QUERY.format(where=where_clause))
        rows = cur.fetchall()
        activities = []
        for row in rows:
            activities.append(ContributorActivity(
                date=row[0],
                team_name=row[1],
                source_name=row[2],
                total=row[3],
                new=row[4],
            ))

        ContributorActivity.objects.bulk_create(activities)
        print 'Created {0} contributor activity rows'.format(len(rows))

    except MySQLdb.Error as e:
        sys.stderr.write('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()
