#!/usr/bin/env python
import os
from optparse import OptionParser

from jinja2 import Template


HEADER = '!!AUTO-GENERATED!! Edit {template}.tmpl instead.'
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etc', 'cron.d'))
LOG_DIR = os.getenv('CRON_LOG_DIR', '/var/log/bedrock')


def main():
    parser = OptionParser()
    parser.add_option('-w', '--webapp',
                      help='Location of web app (required)')
    parser.add_option('-s', '--source',
                      help='Location of source for the web app (required)')
    parser.add_option('-t', '--template',
                      help='Name of the template (e.g. bedrock-prod)')
    parser.add_option('-u', '--user', default='root',
                      help=('Prefix cron with this user. '
                            'Only define for cron.d style crontabs.'))
    parser.add_option('-p', '--python', default='python2.6',
                      help='Python interpreter to use.')

    (opts, args) = parser.parse_args()

    if not opts.webapp:
        parser.error('-w must be defined')

    if not opts.template:
        parser.error('-t must be defined')

    # ensure log path exists
    if not os.path.isdir(LOG_DIR):
        try:
            os.mkdir(LOG_DIR)
        except OSError:
            parser.error('failed to create log directory: ' + LOG_DIR)

    log_file = 'cron-{0}.log'.format(opts.template.split('-')[1])
    django_manage = 'cd {{dir}} && {py} manage.py'.format(py=opts.python)
    django_cron = '{0} cron'.format(django_manage)
    ctx = {
        'log': '>> {0}/{1}.log 2>&1'.format(LOG_DIR, log_file),
        'django_manage': django_manage.format(dir=opts.webapp),
        'django_src_manage': django_manage.format(dir=opts.source),
        'django_cron': django_cron.format(dir=opts.webapp),
    }

    for k, v in ctx.iteritems():
        ctx[k] = '%s %s' % (opts.user, v)

    # Needs to stay below the opts.user injection.
    ctx['user'] = opts.user
    ctx['webapp'] = opts.webapp
    ctx['source'] = opts.source
    ctx['python'] = opts.python
    ctx['header'] = HEADER.format(template=opts.template)

    tmpl_final_name = os.path.join(TEMPLATE_DIR, opts.template)
    tmpl_src_name = tmpl_final_name + '.tmpl'
    tmpl_temp_name = tmpl_final_name + '.TEMP'
    try:
        with open(tmpl_src_name, 'r') as src_fh:
            with open(tmpl_temp_name, 'w') as out_fh:
                out_fh.write(Template(src_fh.read()).render(**ctx))
    except IOError:
        parser.error('file must exist: ' + tmpl_src_name)

    # atomically move into place
    os.rename(tmpl_temp_name, tmpl_final_name)


if __name__ == '__main__':
    main()
