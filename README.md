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
