# Developer notes

Things to bear in mind when working on localisation of Pocket-mode pages
## Translation service

For Pocket pages, all translations are handled by a vendor, rather than the community.
## Namespacing

Please ensure all strings for Pocket templates are use `pocket-` at the start of their name. While there should be no clashes because the Mozorg and Pocket L10N configs are independent, this will give us extra protection and make discovery and replacement easier.
