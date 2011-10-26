import jinja2
import jingo
from django.template.loader import render_to_string

from jingo import register
from product_details import product_details


def latest_aurora_version(locale):
    builds = product_details.firefox_primary_builds
    vers = product_details.firefox_versions['FIREFOX_AURORA']

    if locale in builds:
        if vers in builds[locale]:
            return (vers, builds[locale])

    return None


def latest_beta_version(locale):
    builds = product_details.firefox_primary_builds
    vers = product_details.firefox_versions['LATEST_FIREFOX_DEVEL_VERSION']

    if locale in builds:
        if vers in builds[locale]:
            return (vers, builds[locale])

    return None


def latest_version(locale):
    beta_vers = product_details.firefox_versions['FIREFOX_AURORA']
    aurora_vers = product_details.firefox_versions['LATEST_FIREFOX_DEVEL_VERSION']

    def _check_builds(builds):
        if locale in builds and isinstance(builds[locale], dict):
            lst = builds[locale].items()
            lst.reverse()

            for version, info in lst:
                if version == beta_vers or version == aurora_vers:
                    continue
                if info:
                    return (version, info)
        return None

    return (_check_builds(product_details.firefox_primary_builds) or
            _check_builds(product_details.firefox_beta_builds))


@register.function
@jinja2.contextfunction
def download_button(ctx, locale, build=None):

    def download_html(version, locale, platform):
        return """
<li class="%s">
  <a class="download-link download-%s" href="">
    <span class="download-content">
      <span class="download-title"></span>
      
    </span>
  </a>
</li>
"""
    
    def _version(locale):
        if build == 'aurora':
            return latest_aurora_version(locale)
        elif build == 'beta':
            return latest_beta_version(locale)
        else:
            return latest_version(locale)

    (version, platforms) = _version(locale) or _version('en-US')

    html = """
"""

    jshtml = []

    for platform in ['Windows', 'Linux', 'OS X']:
        if platform in platforms:
            jshtml.append(download_html(version, locale, platform))
        else:
            jshtml.append(download_html(version, 'en-US', platform))
    
    langs = product_details.languages
    locale_name = langs[locale]['native'] if locale in langs else ''
    
    html = render_to_string('mozorg/download_button.html',
                            {'locale_name': locale_name,
                             'test': lambda x: 5})
    return jinja2.Markup(html)
