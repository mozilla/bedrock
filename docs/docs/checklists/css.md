## Responsive

- [ ] CSS written mobile-first
- [ ] In extremely wide viewports, the edges of backgrounds are not visible
- [ ] In narrow viewports, content stacks in a logical reading order
- [ ] Conditional content displays under correct conditions (logged in, out, Fx, not Fx)

## Best practices

- [ ] Passes Stylelint
- [ ] Components added locally do NOT use `mzp` prefix on classes
    - [ ] Can still use [other prefix conventions](https://protocol.mozilla.org/docs/contributing/naming)
- [ ] Prefer classes over element selectors or IDs
- [ ] Use mixins and design tokens when available
- [ ] No commented out code


## Localization

- [ ] Test in a RTL language (You may find the [Pseudolocalize addon](https://addons.mozilla.org/en-US/firefox/addon/pseudolocalize/) helpful.)
- [ ] BIDI mixin used for any properties which include `left` or `right`
- [ ] BIDI mixin used for any properties which assume LTR (e.g. `background-position`, shorthands like `border-width`)
- [ ] BIDI mixin used for any values which include `left` or `right`
