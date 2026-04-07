import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _load_dotenv_if_present(env_path: Path) -> None:
    """
    Minimal .env loader (no external dependency).

    Supports simple KEY=VALUE pairs and ignores comments.
    """
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


_load_dotenv_if_present(BASE_DIR / ".env")

try:
    import dj_database_url  # type: ignore

    _HAS_DJ_DATABASE_URL = True
except ModuleNotFoundError:
    _HAS_DJ_DATABASE_URL = False

try:
    import whitenoise  # noqa: F401

    _HAS_WHITENOISE = True
except ModuleNotFoundError:
    _HAS_WHITENOISE = False


SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-dev-secret-key")
DEBUG = _get_bool("DEBUG", default=False)

ALLOWED_HOSTS = _split_csv(os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1"))


INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Local apps (use explicit AppConfig to avoid needing __init__.py files)
    "apps.core.apps.CoreConfig",
    "apps.treatments.apps.TreatmentsConfig",
    "apps.testimonials.apps.TestimonialsConfig",
    "apps.blog.apps.BlogConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

if _HAS_WHITENOISE:
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL:
    if _HAS_DJ_DATABASE_URL:
        # Production-style DATABASE_URL (Render/DO/Heroku)
        DATABASES = {
            "default": dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                ssl_require=not DEBUG,
            )
        }
    else:
        # dj_database_url isn't installed in this environment.
        # Fall back to sqlite so the project can still start.
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
else:
    # Local development-style DB_* variables (see .env.example)
    DB_NAME = os.environ.get("DB_NAME", "")
    if DB_NAME:
        DATABASES = {
            "default": {
                "ENGINE": os.environ.get(
                    "DB_ENGINE", "django.db.backends.postgresql"
                ),
                "NAME": os.environ.get("DB_NAME", "loya_eye_db"),
                "USER": os.environ.get("DB_USER", "postgres"),
                "PASSWORD": os.environ.get("DB_PASSWORD", ""),
                "HOST": os.environ.get("DB_HOST", "localhost"),
                "PORT": os.environ.get("DB_PORT", "5432"),
                "CONN_MAX_AGE": 600,
            }
        }
    else:
        # Last-resort fallback so the project can still start.
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


if not DEBUG and _HAS_WHITENOISE:
    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )


EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = _get_bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "noreply@example.com"
)


CSRF_TRUSTED_ORIGINS = _split_csv(os.environ.get("CSRF_TRUSTED_ORIGINS", ""))


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

