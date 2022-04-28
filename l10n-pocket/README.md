# Developer notes

Things to bear in mind when working on localisation of Pocket-mode pages
## Translation service

For Pocket pages, all translations are handled by a vendor, rather than the community.
## Namespacing

Please ensure all strings for Pocket templates are use `pocket-` at the start of their name. This will give us extra protection against string name clashes - while Pocket strings should live in this `l10n-pocket/` dir, we are currently having to load some files from regular/mozorg `l10n/`.
