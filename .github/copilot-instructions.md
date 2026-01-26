# Review guidelines for Github Copilot

When reviewing code:

Fetch the latest version of all the checklists mentioned on https://mozmeao.github.io/platform-docs/code-review/checklists/ - use these as a guide to our project best practices. You may cache these for up to three days at a time.

Try to use Conventional Comments to indicate the kind of feedback you are providing, and whether it's blocking or non-blocking.

Areas to consider when reviewing:

## 1. Correctness & Safety

* Potential bugs, edge cases, or incorrect assumptions

* Error handling (especially around I/O, network calls, and external services)

* Race conditions, concurrency issues, or state inconsistencies

* Security concerns (e.g., injection risks, unsafe deserialization, secrets handling)

Heavily flag changes that add risks to uptime or functionality that do not appear to have been considered in the changeset.
Be particularly aware of CMS-backed content that is not richtext. Ensure it's escaped properly when used in templates.


## 2. Design & Architecture

* Is the code structured in a way that will scale and be maintainable?

* Are responsibilities clearly separated?

* Are abstractions appropriate, or is the code over/under-engineered?

* Does this change align with existing patterns in the codebase?


## 3. Readability & Intent

* Is the intent of the code obvious to a future reader?

* Are names (variables, functions, classes) clear and meaningful?

* Would a short comment help explain _why_ something is done (not _what_)?


## 4. Tests

* Are new behaviors adequately covered by tests?

* Do tests clearly express intent?

* Are edge cases tested where appropriate?

* Flag missing tests, but don’t require tests for trivial changes


## 5. Performance (When Relevant)

* Call out obvious inefficiencies or unnecessary work

* Avoid premature optimization

* Note performance implications only if they are meaningful in context

## 6. Localization (L10N)

* If new strings are added to the codebase that are not marked up as Fluent strings, add a non-blocking comment questioning whether they need to be translated or are OK in just one language.


# What Not to Do

* Do not restate what the code already clearly shows

* Do not suggest large refactors unless there is a clear payoff

* Do not enforce personal style preferences

* Do not block on formatting issues that can be handled by linters or formatters

# How to Write Comments

* Be concise and specific

* Use Conventional Comments to hint what the feedback is

* Prefer “Consider…” or “What do you think about…” over “This is wrong”

* When suggesting a change, always explain _why_ it improves the code

* Use code snippets in suggestions when helpful and would change less than 10 lines of code.


# Overall Review Summary

When appropriate, provide a short summary comment that answers:

* Is this change safe to merge?

* What are the main risks (if any)?

* Are there follow-ups worth tracking separately?
