from jingo import register
from product_details import product_details

@register.function
def download_button():
    return product_details.firefox_versions['LATEST_FIREFOX_VERSION']
