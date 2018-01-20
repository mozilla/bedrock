"""
We need this command because we need to clear out the entire
database during a deployment of the demo servers, but we
can't drop the whole DB and recreate because our user doesn't
have the permission, and we don't want it to have permission.

It needs to do it this way because we need it to delete all
tables regardless of whether they're modeled in the currently
deployed code.
"""

from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import connection, transaction


class Command(NoArgsCommand):
    help = 'Delete all the database tables.'
    option_list = NoArgsCommand.option_list + (
        make_option('--yes-i-am-sure',
                    action='store_true',
                    dest='do_it',
                    default=False,
                    help='Delete all the database tables'),
    )

    def handle_noargs(self, **options):
        if options['do_it']:
            print('Deleting tables:')
            cursor = connection.cursor()
            cursor.execute('show tables')
            tables = [row[0] for row in cursor.fetchall()]
            if tables:
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
                for table in tables:
                    print(' - ' + table)
                    cursor.execute('DROP TABLE %s;' % table)
                cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
                transaction.commit_unless_managed()
            else:
                print(' - No tables found. Odd.')
            print('Done.')
        else:
            print("This deletes ALL THE THINGS! If you're sure you " \
                  "want to do this, pass the --yes-i-am-sure flag.")
