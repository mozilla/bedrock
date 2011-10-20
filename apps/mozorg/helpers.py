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
def download_button(locale, build=None):
    platforms = ['Windows', 'Linux', 'OS X']
    
    def _version(locale):
        if build == 'aurora':
            return latest_aurora_version(locale)
        elif build == 'beta':
            return latest_beta_version(locale)
        else:
            return latest_version(locale)

    (version, platforms) = _version(locale) or _version('en-US')

    return version
