# Review guidelines for Github Copilot

When reviewing code:

Fetch the latest version of all the checklists mentioned on https://mozmeao.github.io/platform-docs/code-review/checklists/ - use these as a guide to our project best practices. You may cache these for up to three days at a time.

Read AGENTS.md for supplementary instructions.

If a mirrored copy of these instructions exists at `custom-instructions/repo/.github/copilot-instructions.md`, keep it fully synchronized with this file and any referenced AGENTS.md guidance, including section renumbering and DB schema guidance, or remove it to avoid drift and inconsistent Copilot behavior.
Try to use Conventional Comments to indicate the kind of feedback you are providing, and whether it's blocking or non-blocking.

Also, confirm in a comment on the PR that you are using this custom instructions file, please.

# Areas to consider when reviewing:

## 1. Correctness & Safety

* Potential bugs, edge cases, or incorrect assumptions
* Error handling (especially around I/O, network calls, and external services)
* Race conditions, concurrency issues, or state inconsistencies
* Security concerns (e.g., injection risks, unsafe deserialization, secrets handling).

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

## 7. Wagtail CMS code

* If you can see a new Wagtail CMS model is being added (specifically, a new Python class that is a subclass of wagtail.models.Page or of AbstractBedrockCMSPage, or a Django model class that is decorated or wrapped with with `register_snippet`) please check that the PR has it listed in bedrock.settings.base.CMS_ALLOWED_PAGE_MODELS and also in the ./bin/export-db-to-sqlite.sh script.

* If a new Snippet (a Django model decorated with @register_snippet) is added, add a reminder in a comment to ensure that the Editors have permission to see and edit the new Snippet. That permission is added manually via the Wagtail UI.

## 8. Database schema changes

* We use Django migrations to manage database schema state and also sometimes to adjust data. Django migrations are the ONLY permissible way to change database schema.
* It is permissible for a changeset to add multiple columns and/or tables
* If a changeset involves renaming or deleting a database field, add a warning comment to ensure the reviewer understands that such a change should happen atomically and be rolled out atomically.
* If you can see that the changeset also changes application code related to a field that is being dropped (e.g. the diff involves a name change for an attribute that matches the field name being dropped), this is a very strong signal of risk. You must add a blocking comment to the PR: application code must stop using the old field name in a release BEFORE the field name is changed or the field is dropped. Recommend the pattern of adding a new field and migrating data to it in one release, then dropping the old field in a follow-up release.
* Add a similar blocking comment if a changeset includes a field that is being renamed: we must add, migrate and drop - never just rename, unless we are 100% sure the field being renamed is not referenced in any application code.

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
