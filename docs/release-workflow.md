# Automated Release Workflow

The release workflow (`.github/workflows/release.yml`) automates the full Bedrock deployment pipeline — from preflight checks through to production — replacing the previous 12-step manual process.

## Prerequisites

Before using the workflow, the following must be in place:

### GitHub secret

| Secret name | What it is |
|---|---|
| `BEDROCK_GHA_RELEASE_WORKFLOW_PAT` | A **classic** GitHub Personal Access Token with `repo` scope, belonging to a user who has write access to `mozilla/bedrock`. Must be [authorised for the mozilla org's SAML SSO](https://docs.github.com/en/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on). This PAT is used to push to the `stage` and `prod` branches, and to push release tags. A fine-grained PAT will **not** work — classic PAT only. |

The following secrets must also exist (they power Slack notifications and are already configured):

| Secret name | Purpose |
|---|---|
| `SLACK_BOT_TOKEN_FOR_MEAO_NOTIFICATIONS_APP` | Bot token for posting to Slack |

## Triggering a release

1. Go to **Actions → Release** in the GitHub UI (or navigate to `.github/workflows/release.yml`)
2. Click **Run workflow**
3. Choose whether to **pause on staging** (see below)
4. Click **Run workflow**

The workflow runs only on `mozilla/bedrock` — it is a no-op on forks.

### The `pause_on_staging` option

| Value | Behaviour |
|---|---|
| `true` (default) | The workflow pauses after stage deployment and integration tests pass. A prod reviewer must approve before prod deployment begins. Use this when you want to manually QA on staging first. |
| `false` | The workflow proceeds automatically from stage to prod once all stage checks pass. Use this for routine releases where you're confident in the staged changes. |

## What the workflow does

The workflow runs five jobs in sequence:

```
Preflight checks → Deploy to stage → [Awaiting prod approval] → Deploy to production → Notify completion
```

### 1. Preflight checks

Captures the HEAD SHA of `main` at trigger time (`RELEASE_SHA`) and verifies:

- **Unit tests** passed for `RELEASE_SHA` on `main`
- **Pre-commit standards** passed for `RELEASE_SHA` on `main`
- **Docker image build** completed successfully for `RELEASE_SHA` on `main`
- **Integration tests** for `main`/dev completed successfully for `RELEASE_SHA`

Posts a "Starting release" message to `#www` and `#www-notify` in Slack.

If any CI run for `RELEASE_SHA` was **cancelled** (typically because a new commit landed on `main` mid-run), the workflow aborts with a clear message asking you to re-trigger once `main` is stable.

### 2. Deploy to stage

- Pushes `RELEASE_SHA` to the `stage` branch
- Waits for the Docker image build on `stage` to complete
- Waits for **both** integration test runs on stage to succeed (dispatched automatically by the deployment infrastructure)
- Posts a "Pushing to Bedrock stage" message to `#www`

### 3. Awaiting prod approval *(only when `pause_on_staging=true`)*

The workflow pauses here. Any member of the `prod` environment's reviewer list (see [Managing prod reviewers](#managing-prod-reviewers) below) can approve via:

1. The yellow banner on the workflow run page → **View** → **Approve**
2. Or via the GitHub notification email

### 4. Deploy to production

- Checks out exactly `RELEASE_SHA` (not the current HEAD of `main`, which may have advanced during staging)
- Runs `bin/tag-release.sh --ci --push` to create a `YYYY-MM-DD[.X]` tag and push it and `RELEASE_SHA` to the `prod` branch
- Waits for the Docker image build for the tag to complete
- Waits for **both** integration test runs on prod to succeed
- Posts "Pushing Bedrock Prod, tagged `YYYY-MM-DD[.X]`" and confirmation to `#www`

### 5. Notify completion

Always runs regardless of outcome. Posts a final success or failure summary to both `#www` and `#www-notify`.

## Behaviour when `main` is busy

- **During preflight:** if a new commit lands on `main` and cancels the CI for `RELEASE_SHA`, the workflow aborts with an explanatory message. Re-trigger once `main` is stable.
- **During or after staging:** new commits on `main` do not affect the release. The workflow always deploys exactly `RELEASE_SHA` — the SHA that was captured at trigger time and tested on stage.

## What to do if the workflow fails

| Failure point | Likely cause | Action |
|---|---|---|
| Preflight — unit tests/pre-commit cancelled | New commit landed on `main` | Wait for `main` to stabilise, re-trigger |
| Preflight — unit tests/pre-commit failed | Real CI failure | Fix the failure on `main` first |
| Preflight — Docker build failed | Build error | Check the build-and-push workflow run |
| Preflight — integration tests failed | Test failure on dev | Investigate or proceed manually if known-flaky |
| Deploy to stage — push failed | PAT permissions issue | Check `BEDROCK_GHA_RELEASE_WORKFLOW_PAT` is valid and SAML-authorised |
| Deploy to stage — integration tests failed | Test failure on stage | Investigate before proceeding |
| Deploy to prod — tag-release.sh failed | `main` ≠ `stage` (someone pushed to `stage` manually) | Investigate; re-trigger if safe |
| Any step timed out | Infra issue / deployment took too long | Check the relevant workflow run; re-trigger if appropriate |

If the workflow aborts after the tag has been pushed but before integration tests pass, the tag and prod branch **have** been updated. Check the production environment and proceed manually if needed.

## Managing prod reviewers

When `pause_on_staging=true`, the workflow pauses at the **"Awaiting prod approval"** step until a reviewer approves. The current reviewers are:

- **Team:** `mozilla/bedrock-team` (all members can approve)
- **Individual users:** `maureenlholland`, `wen-2018`, `bluewave41`, `kkellydesign`

### Adding or removing reviewers

Use the GitHub API. You must supply the **complete** reviewer list each time (the call replaces, not appends).

**Get current team/user IDs:**

```bash
# Team ID
gh api orgs/mozilla/teams/bedrock-team --jq '.id'

# User ID
gh api users/<github-username> --jq '.id'
```

**Update the reviewer list:**

```bash
gh api repos/mozilla/bedrock/environments/prod \
  --method PUT \
  --input - <<'EOF'
{
  "reviewers": [
    {"type": "Team", "id": 75128},
    {"type": "User", "id": 19650432},
    {"type": "User", "id": 42974891},
    {"type": "User", "id": 9813994},
    {"type": "User", "id": 202590}
  ]
}
EOF
```

Replace or extend the `reviewers` array as needed. The current IDs are:

| Reviewer | Type | ID |
|---|---|---|
| `mozilla/bedrock-team` | Team | `75128` |
| `maureenlholland` | User | `19650432` |
| `wen-2018` | User | `42974891` |
| `bluewave41` | User | `9813994` |
| `kkellydesign` | User | `202590` |

You can also manage reviewers in the GitHub UI at:
**Repository Settings → Environments → prod → Edit**
