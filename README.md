# Python QM base

Public dependency image for Python 3.13, Django 5.2, PostgreSQL and scientific calculations.
Contains only public open-source dependencies. No application code, business data, company endpoints or credentials.

## Build and publish

Pushes to main build on a standard GitHub-hosted Ubuntu runner (free for public repositories).
Pull requests build and run offline checks without publishing. Manual builds are available in Actions.
No self-hosted runner or manually configured secrets are required: publishing uses the built-in GITHUB_TOKEN.

The build installs requirements.txt, checks dependency compatibility and exercises imports, NumPy, SciPy,
the binary PostgreSQL driver and Django with an in-memory database. It does not replace application or PostgreSQL integration tests.
The smoke test runs with network access disabled. Only successful images are published.

Images:
- ghcr.io/missel2/python-qm-base:sha-COMMIT_SHA — commit-specific tag
- ghcr.io/missel2/python-qm-base:deps-v1 — moving convenience tag

Target: linux/amd64. Direct dependencies are version-pinned. Transitive dependencies and the Python base tag
can change on rebuild; this is not a bit-for-bit reproducible build. Installed versions are recorded inside
the image at /opt/python-qm-base/installed.txt. Pin a tested registry digest for deployment.

## First publication: enable anonymous pulls

A public repository does not automatically guarantee a public GHCR package.
After the first successful publication open:
https://github.com/users/Missel2/packages/container/python-qm-base/settings

Under Package settings / Change visibility choose Public.
Public packages can be pulled without credentials. Public package visibility cannot be reverted to private.

## Use as CI image

Replace the Python test job's image with the published commit-specific tag or digest.
Remove the online pip install command, keep the existing PostgreSQL service and all application tests.

```yaml
image: ghcr.io/missel2/python-qm-base:deps-v1
script:
  - python -m pip check
  # Keep the project's existing checks and tests below.
```

Use deps-v1 for initial testing; pin the successfully tested image digest afterward.
Private registries used for mirroring need their own runner pull credentials.

## Use as application build base

Replace the Python FROM line in the application's Dockerfile with this image.
Remove the pip install part of the RUN instruction, preserving account creation and other application setup.
Keep copying the application's requirements.txt and verify that the image still matches it:

```dockerfile
FROM ghcr.io/missel2/python-qm-base:deps-v1
COPY backend/requirements.txt /tmp/application-requirements.txt
RUN python -m pip install --no-index --no-deps -r /tmp/application-requirements.txt \
    && python -m pip check
```

This command uses already-installed packages and fails without downloading if direct versions do not match.
Rebuild this base when application dependency versions change.

This image does not contain Node.js, pnpm or frontend packages. Frontend downloads are a separate concern.
If the target network cannot pull from GHCR, mirror this image into an accessible registry.
