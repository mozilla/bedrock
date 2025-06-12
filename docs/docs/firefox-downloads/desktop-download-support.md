---
render_macros: true
---

## Windows

For Windows, we generally only serve the 32bit stub installer. The reason for this is that the installer can figure out if the OS is 32bit or 64bit more accurately than User Agent strings can be relied upon for. The installer can then trigger the full download for the most appropriate binary. The only exception to this is for Firefox Beta. Here we serve links to the full installer and rely upon 32bit / 64 bit detection at the website level. The reason for this is that only the full installer offers the ability to change the installation path, as by default installing Firefox Beta would override the default location for the release installation of Firefox.

## ChromeOS

[bedrock/issues#8006](https://github.com/mozilla/bedrock/issues/8006)


## Linux

On Linux, we can no longer accurately detect 32bit and 64bit operating systems via User Agent, since those identifiers have now been frozen by browsers such as Firefox. As a result, Linux visitors currently see two download buttons, one for 32bit and one for 64bit. This is not ideal and could be improved with some prioritization. Most Linux users install Firefox via a package manager however, rather than the website.

## Unsupported Operating systems

Firefox is no longer supported on Windows 8.1 and below, as well as on macOS 10.14 and below. For these operating systems we display a Firefox ESR download button that is pinned to Firefox ESR 115, the last ESR release supported on those platforms. The messaging can be found in `bedrock/firefox/templates/firefox/includes/download-unsupported.html` and is shown conditionally when `site.js` adds a class of `fx-unsuppported` to the root `<html>` element, in combination with either `windows` or `osx`.
