- [ ] Consent is respected
- [ ] There is a switch to disable it
- [ ] If there are other conditions to run, bundle the display logic into one variable
    - i.e. `is_enabled = switch('switchname') && geo=US && lang.startswith('en')`
- [ ] Test all variations
- [ ] Test an unexpected variation
- [ ] With the experiment disabled experiment variations do not load
- [ ] With the experiment disabled experiment code is not loaded
- [ ] If a template was added it is `noindex` and has a canonical URL
- [ ] The events which will determine the success of the experiment are being recorded
    - Usually in GA but sometimes Stub Attribution or FundraiseUp
- [ ] An `experiment_view` event is reported in the DataLayer
- [ ] No conflicting experiments

# Traffic Cop experiments

- [ ] Checks `isApprovedToRun` before activating
- [ ] Experiment activation logic is sound
- [ ] Traffic is split between variants as expected
- [ ] [Cookie support is not necessary or is included](https://mozilla.github.io/bedrock/abtest/#cookies-consent)


[Experiment documentation](https://mozilla.github.io/bedrock/abtest/)
