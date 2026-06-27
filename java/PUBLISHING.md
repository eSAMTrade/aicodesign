# Publishing the Java library to Maven Central

The repo is already configured. Maven Central's modern flow (Central Portal) is
self-service — **no multi-day waits**. Namespace verification is ~5 min via DNS;
GPG keys are instant. This guide covers the steps that require your account/browser.

## What's already done (by tooling, in this repo)

- `pom.xml` is Central-ready: groupId `com.esamtrade`, release version `0.1.0`,
  license + developer + SCM metadata, sources jar, javadoc jar, GPG signing, and
  the `central-publishing-maven-plugin`.
- A 4096-bit GPG signing key was generated and its **public key is already published**
  to `keyserver.ubuntu.com` (fingerprint `26366396DA3F1ECE2CEE662FF2C8FE56BBBF7F0D`).
- The private key + passphrase are in `.publish-secrets/` (gitignored — never committed).
- A GitHub Actions workflow `.github/workflows/publish-java.yml` publishes on a `v*` tag.

## Steps you must do (cannot be automated — needs your login)

### 1. Create a Central Portal account
Go to <https://central.sonatype.com> → **Sign In** → log in with the **eSAMTrade GitHub
account** (or email).

### 2. Register and verify the `com.esamtrade` namespace
- In the Portal: **Namespaces → Add Namespace** → enter `com.esamtrade`.
- It shows a **Verification Key** (a random string).
- Add a **DNS TXT record** on `esamtrade.com`:
  - **Host/Name:** `@` (i.e. `esamtrade.com`)
  - **Type:** `TXT`
  - **Value:** the verification key from the Portal
- Wait ~5 min for DNS to propagate, then click **Verify Namespace**. Status → `VERIFIED`.

### 3. Generate a publishing token
Portal → **your account → Generate User Token** → copy the **username** and **password**
it shows (you only see the password once).

### 4. Add four GitHub repository secrets
Repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret name              | Value |
|--------------------------|-------|
| `CENTRAL_TOKEN_USERNAME` | token username from step 3 |
| `CENTRAL_TOKEN_PASSWORD` | token password from step 3 |
| `GPG_PRIVATE_KEY`        | full contents of `.publish-secrets/private-key.asc` |
| `GPG_PASSPHRASE`         | the line in `.publish-secrets/gpg_passphrase.txt` |

### 5. Publish
Commit & push the repo changes, then push a release tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The workflow signs the artifacts and uploads them. With `autoPublish=true` the release
goes live on Maven Central automatically (searchable in ~15–30 min). Done.

---

## Alternative: publish from your laptop (no GitHub Actions)

Requires Maven (`brew install maven` / `apt install maven`) and the GPG key imported
locally (`gpg --import .publish-secrets/private-key.asc`).

Add the token to `~/.m2/settings.xml`:

```xml
<settings>
  <servers>
    <server>
      <id>central</id>
      <username>TOKEN_USERNAME</username>
      <password>TOKEN_PASSWORD</password>
    </server>
  </servers>
</settings>
```

Then:

```bash
cd java
mvn -B deploy -Dgpg.passphrase="$(cat ../.publish-secrets/gpg_passphrase.txt)"
```

---

## Fallback: GitHub Packages (not recommended for a public library)

Works without Sonatype, but **every consumer must authenticate with a GitHub PAT just to
download the jar** — poor UX for an open-source library. Only use if Central is blocked.

1. Restore a `<distributionManagement>` block in `pom.xml` pointing at
   `https://maven.pkg.github.com/eSAMTrade/aicodesign` (id `github`).
2. Add a `github` server to `~/.m2/settings.xml` with your GitHub username + a PAT
   that has `write:packages`.
3. `cd java && mvn deploy`.

Consumers then need the repository block + a `read:packages` PAT in their own settings.
