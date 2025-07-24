## Links `<a>`

- [ ] Has a `data-cta-text` OR `data-link-text`
    - [ ] If it has class `mzp-c-button` it is a CTA
    - [ ] If it has class `mzp-c-cta-link` it is a CTA
    - [ ] If there are two of the same `data-cta-text` include `data-cta-position`
    - [ ] Does not have both `data-cta-text` and `data-link-text`
- [ ] If linking to another Mozilla property include `utm` params
- Download button:
    - [ ] Use the appropriate helper, don't hard code these. (`download_firefox_thanks`, `google_play_button`, `apple_app_store_button`)
    - [ ] include a download_location if there are multiple buttons on the page

# Buttons `<button type="button">`

- Download button:
    - Download buttons are links, see above
- Not a download button:
    - [ ] [`widget_action` reporting in the dataLayer](https://mozilla.github.io/bedrock/attribution/0001-analytics/#widget-action)

# QR Codes

-  [ ] Use the `qr_code` helper
-  [ ] Use the apps store redirects if applicable - include a product and campaign

# Other

- [ ] New custom events configured in GTM.
- If any of the following are used check that their custom events will be triggered:
    - Download
    - Mozilla Accounts form
    - Newsletter subscribe
    - Self-hosted videos
    - Send to Device
    - Social Share
    - VPN subscribe button
    - Widget Action
