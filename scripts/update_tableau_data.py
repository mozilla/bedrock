import urlparse
import sys

from django.conf import settings

try:
    import MySQLdb
except ImportError:
    # not everyone needs the mysql lib, but this function needs it.
    # we'll pass here and fail later so tests can work.
    MySQLdb = None

from bedrock.mozorg.models import ContributorActivity


urlparse.uses_netloc.append('mysql')
QUERY = ('SELECT c_date, team_name, source_name, count(*) AS total, IFNULL(SUM(is_new), 0) AS new '
         'FROM contributor_active {where} GROUP BY c_date, team_name, source_name')


def process_name_fields(team_name):
    """Lowercase and remove spaces"""
    return team_name.replace(' ', '').lower()


def get_external_data():
    """Get the data and return it as a tuple of tuples."""
    if not settings.TABLEAU_DB_URL:
        print('Must set TABLEAU_DB_URL.')
        sys.exit(1)

    url = urlparse.urlparse(settings.TABLEAU_DB_URL)
    if not url.path:
        # bad db url
        print('TABLEAU_DB_URL not parseable.')
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
        return cur.fetchall()
    except MySQLdb.Error as e:
        sys.stderr.write('Error %d: %s' % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()


def run():
    """Get contributor activity data from Tableau and insert it into bedrock DB."""
    activities = []
    for row in get_external_data():
        activities.append(ContributorActivity(
            date=row[0],
            team_name=process_name_fields(row[1]),
            source_name=process_name_fields(row[2]),
            total=row[3],
            new=row[4],
        ))

    ContributorActivity.objects.bulk_create(activities)
