"""Exercise the installed dependencies without application code or network access."""
from importlib.metadata import version
import math
import platform

import django
import numpy as np
import psycopg
from psycopg import pq
from scipy import stats
from django.conf import settings
from django.db import connection

expected = {
    "Django": "5.2.18", "psycopg": "3.2.12", "gunicorn": "23.0.0",
    "whitenoise": "6.11.0", "numpy": "2.3.5", "scipy": "1.17.0",
}
assert platform.python_version_tuple()[:2] == ("3", "13")
for package, wanted in expected.items():
    actual = version(package)
    assert actual == wanted, (package, actual, wanted)
    print(f"{package}={actual}", flush=True)

assert pq.__impl__ == "binary", pq.__impl__
assert pq.version() > 0
values = np.array([11.3, 12.1, 13.0])
assert math.isclose(float(np.mean(values)), 12.133333333333333)
assert math.isclose(float(stats.norm.cdf(0)), 0.5)
settings.configure(
    SECRET_KEY="offline-smoke-test-only",
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    INSTALLED_APPS=[],
)
django.setup()
with connection.cursor() as cursor:
    cursor.execute("SELECT 1")
    assert cursor.fetchone() == (1,)
print("Offline dependency smoke test passed.", flush=True)
