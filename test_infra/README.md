# CDN Tests

These tests will look for things like the geolocation endpoint functioning properly, the right headers being returned, the requests to `/media/*` coming from the S3 origin, etc. To run them issue the following command:

```
$ make TEST_DOMAIN=www.mozorg.moz.works test-cdn
```

This will download the TLS report if you don't already have it and run the tests against the `TEST_DOMAIN` you add to the command. If you don't include `TEST_DOMAIN` in the command it defaults to `www.mozilla.org`. If you'd like to download a new TLS report just `rm test_infra/fixtures/tls.json` and run it again.

> NOTE: The TLS report download will take a few minutes.
