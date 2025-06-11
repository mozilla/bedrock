---
render_macros: true
---

The stub installer is has been configured to serve a version of Firefox that will set itself as the default
browser during installation if the stub attribution code includes the campaign value `SET_DEFAULT_BROWSER`.

Using stub attribution this way means it cannot be used for acquisition data, though it will still include
the analytics session IDs if they are present.

At the moment (2025-06-10) if the switch `download_as_default` is enabled a checkbox should
appear for users who match the following criteria:

- their device supports stub attribution
- they are not in the EU/EAA
- they have not explicitly declined cookies
- they have not enabled GCP or DNT
- their device supports Firefox
- their device is running a version of Windows higher than 8.1

If they match the criteria a script will:

- reveal the checkboxes
- strip utm parameters from the URL
- update the URL to include the `SET_DEFAULT_BROWSER` campaign parameter
- refresh stub attribution to reflect the updated url

Unchecking the checkbox will not revert to the previous value of the stub attribution code.

Note that it is permitted by EU/EAA law to send the campaign parameter in response to an explicit
user action so we may enable this for `needs_data_consent` countries in the future.
