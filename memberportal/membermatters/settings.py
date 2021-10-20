"""
Django settings for membermatters project.

Generated by "django-admin startproject" using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
from collections import OrderedDict
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get(
    "PORTAL_SECRET_KEY", "l)#t68rzepzp)0l#x=9mntciapun$whl+$j&=_@nl^zl1xm3j*"
)

# Default config is for dev environments and is overwritten in prod
DEBUG = True
ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# this allows the frontend dev server to talk to the dev server
CORS_ALLOW_ALL_ORIGINS = True

if os.environ.get("PORTAL_ENV") == "Production":
    ENVIRONMENT = "Production"
    CORS_ALLOW_ALL_ORIGINS = False
    DEBUG = False

# Application definition
INSTALLED_APPS = [
    "constance",
    "constance.backends.database",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "profile",
    "access",
    "group",
    "memberbucks",
    "api_spacedirectory",
    "api_general",
    "api_access",
    "api_meeting",
    "api_admin_tools",
    "api_billing",
    "corsheaders",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "membermatters.middleware.Sentry",
    "membermatters.middleware.ForceCsrfCookieMiddleware",
]

ROOT_URLCONF = "membermatters.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "constance.context_processors.config",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "membermatters.wsgi.application"

if "MMDB_SECRET" in os.environ:
    # This is a JSON blob containing the database connection details, generated by "copilot" in an AWS deployment
    # Fields in this JSON blob are: {username, host, dbname, password, port}
    database_config = json.loads(os.environ["MMDB_SECRET"])
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": database_config.get("dbname"),
            "USER": database_config.get("username"),
            "PASSWORD": database_config.get("password"),
            "HOST": database_config.get("host"),
            "PORT": database_config.get("port"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("PORTAL_DB_LOCATION", "/usr/src/data/db.sqlite3"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.environ.get(
                "PORTAL_LOG_LOCATION", "/usr/src/logs/django.log"
            ),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "membermatters.custom_exception_handlers.fix_401",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,
    "UPDATE_LAST_LOGIN": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": "Bearer",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-au"

TIME_ZONE = "Australia/Brisbane"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.environ.get(
    "PORTAL_STATIC_LOCATION", "/usr/src/app/memberportal/membermatters/static"
)
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/signin"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("PORTAL_MEDIA_LOCATION", "/usr/src/data/media/")

AUTH_USER_MODEL = "profile.User"

REQUEST_TIMEOUT = 0.05

# Django constance configuration
CONSTANCE_BACKEND = "membermatters.constance_backend.DatabaseBackend"

CONSTANCE_CONFIG = {
    # General site info
    "SITE_NAME": (
        "MemberMatters Portal",
        "The title shown at the top of the page and as the tab title.",
    ),
    "SITE_OWNER": (
        "MemberMatters",
        "The name of the legal entity/association/club that is running this site.",
    ),
    "ENTITY_TYPE": (
        "Association",
        "This is the type of group you are such as an association, club, etc.",
    ),
    # Email config
    "EMAIL_SYSADMIN": (
        "example@example.com",
        "The default sysadmin email that should receive technical errors etc.",
    ),
    "EMAIL_ADMIN": (
        "example@example.com",
        "The default admin email that should receive administrative notifications.",
    ),
    "EMAIL_DEFAULT_FROM": (
        '"MemberMatters Portal" <example@example.org>',
        "The default email that outbound messages are sent from.",
    ),
    "SITE_MAIL_ADDRESS": (
        "123 Example St, Nowhere",
        "This address is used in the footer of all emails for anti spam.",
    ),
    # URLs
    "SITE_URL": (
        "https://membermatters.org",
        "The publicly accessible URL of your MemberMatters instance.",
    ),
    "MAIN_SITE_URL": ("https://membermatters.org", "The URL of your main website."),
    "CONTACT_PAGE_URL": (
        "https://membermatters.org",
        "The URL of your contact page (displayed during signup if "
        "requireAccessCard == False).",
    ),
    "INDUCTION_URL": (
        "https://eventbrite.com.au",
        "The URL members should visit to book in for a site induction.",
    ),
    # Logo and favicon
    "SITE_LOGO": (
        "https://hsbne-public-assets.s3-ap-southeast-2.amazonaws.com/main-logo.png",
        "Site logo (rectangular)",
    ),
    "SITE_FAVICON": (
        "https://hsbne-public-assets.s3-ap-southeast-2.amazonaws.com/logo-favicon.png",
        "Site favicon (square)",
    ),
    "STATS_CARD_IMAGE": (
        "https://hsbne.org/assets/img/carousel/00.jpg",
        "Image to use for the site statistics card.",
    ),
    "MENU_BACKGROUND": (
        "",
        "[Optional] Image to use as the background in the menu. Leave blank for the default background image.",
    ),
    # Custom theme colors
    "THEME_PRIMARY": ("#278ab0", "Custom primary theme colour"),
    "THEME_TOOLBAR": ("#0461b1", "Custom toolbar theme colour"),
    "THEME_ACCENT": ("#189ab4", "Custom accent theme colour"),
    # Localisation of terminology
    "MEMBERBUCKS_NAME": (
        "Memberbucks",
        "You can customise the name of the built in currency.",
    ),
    "GROUP_NAME": ("Group", "You can customise what we call a group."),
    "ADMIN_NAME": (
        "Administrators",
        "You can specify a different name for your admin group like executive or management committee.",
    ),
    "WEBCAM_PAGE_URLS": (
        "[]",
        "A JSON serialised array of URLs to pull webcam images from.",
    ),
    "HOME_PAGE_CARDS": (
        """[
            {
                "title": "Example",
                "description": "This is an example card with a narwhal icon!",
                "icon": "fad fa-narwhal",
                "url": "https://membermatters.org/",
                "btn_text": "Click Here"
            },
            {
                "title": "Example 2",
                "description": "This is an example card with a unicorn icon! And it links to another page using a Vue route!",
                "icon": "fad fa-unicorn",
                "routerLink": {
                "name": "reportIssue"
                },
                "btn_text": "Go to route"
            }
           ]
        """,
        "You can specify cards that go on the home page with JSON. See https://github.com/MemberMatters/MemberMatters/blob/master/GETTING_STARTED.md.",
    ),
    "WELCOME_EMAIL_CARDS": (
        "[]",
        "Same syntax as HOME_PAGE_CARDS but icons are not used. If nothing is specified we will use HOME_PAGE_CARDS.",
    ),
    # Stripe config
    "STRIPE_PUBLISHABLE_KEY": ("", "Set this to your Stripe PUBLIC API key."),
    "STRIPE_SECRET_KEY": ("", "Set this to your Stripe PRIVATE API key."),
    "STRIPE_WEBHOOK_SECRET": (
        "",
        "Set this to a secret value to verify that a webhook came from Stripe.",
    ),
    "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS": (
        "[1000, 2000, 3000]",
        "This is a JSON array of top-up amounts in cents.",
    ),
    "MAKEMEMBER_CREATE_XERO_INVOICES": (
        False,
        "Creates a Xero invoice when 'Make Member' is clicked in the admin tools area.",
    ),
    "STRIPE_CREATE_XERO_INVOICES": (
        False,
        "Creates an invoice in Xero for every successful Stripe membership payment.",
    ),
    "XERO_TAX_TYPE": ("EXEMPTOUTPUT", "Tax type to use on Xero invoices."),
    "XERO_MEMBERSHIP_ACCOUNT_CODE": (
        "100",
        "Account code to use on Xero invoices for membership.",
    ),
    "XERO_MEMBERSHIP_ITEM_CODE": (
        "membership",
        "Item code to use on Xero invoices for membership.",
    ),
    "XERO_STRIPE_FEE_ACCOUNT_CODE": (
        "100",
        "Account code to use on Xero invoices for membership.",
    ),
    "XERO_STRIPE_FEE_ITEM_CODE": (
        "stripe",
        "Item code to use on Xero invoices for membership.",
    ),
    "XERO_MEMBERBUCKS_ACCOUNT_CODE": (
        "100",
        "Account code to use on Xero invoices for memberbucks.",
    ),
    "ENABLE_STRIPE_MEMBERSHIP_PAYMENTS": (
        False,
        "Enable integration with stripe for membership payments.",
    ),
    # Trello config
    "ENABLE_TRELLO_INTEGRATION": (
        False,
        "Enable the submit issue to trello integration. If disabled we'll send an email to EMAIL_ADMIN instead.",
    ),
    "TRELLO_API_KEY": ("", "Set this to your Trello API key."),
    "TRELLO_API_TOKEN": ("", "Set this to your Trello API token."),
    "TRELLO_ID_LIST": (
        "",
        "Set this to the ID of your card list you want issue " "to go to.",
    ),
    # Space API config
    "SPACE_DIRECTORY_ENABLED": (
        True,
        "Turn on the space directory API available at /api/spacedirectory.",
    ),
    "SPACE_DIRECTORY_OPEN": (False, "Sets the open state."),
    "SPACE_DIRECTORY_MESSAGE": (
        "This is the default MemberMatters (membermatters.org) space directory message.",
        "Sets the message.",
    ),
    "SPACE_DIRECTORY_ICON_OPEN": ("", "Sets the icon shown while in the open state."),
    "SPACE_DIRECTORY_ICON_CLOSED": (
        "",
        "Sets the icon shown while in the closed state.",
    ),
    "SPACE_DIRECTORY_LOCATION_ADDRESS": (
        "123 Setme St",
        "Sets the snail mail address.",
    ),
    "SPACE_DIRECTORY_LOCATION_LAT": (0, "Sets the latitude."),
    "SPACE_DIRECTORY_LOCATION_LON": (0, "Sets the longitude."),
    "SPACE_DIRECTORY_FED_SPACENET": (False, "Sets support for spacenet."),
    "SPACE_DIRECTORY_FED_SPACESAML": (False, "Sets support for spacesaml."),
    "SPACE_DIRECTORY_FED_SPACEPHONE": (False, "Sets support for spacephone."),
    "SPACE_DIRECTORY_CAMS": (
        "[]",
        "A JSON list of strings (URLs) that webcam snapshots of the space can be found.",
    ),
    "SPACE_DIRECTORY_CONTACT_EMAIL": (
        "notset@example.com",
        "Sets the general contact email.",
    ),
    "SPACE_DIRECTORY_CONTACT_TWITTER": ("", "Sets the twitter handle."),
    "SPACE_DIRECTORY_CONTACT_FACEBOOK": ("", "Sets the Facebook page URL."),
    "SPACE_DIRECTORY_CONTACT_PHONE": (
        "",
        "Sets the general contact phone number, include country code with a leading +.",
    ),
    "SPACE_DIRECTORY_PROJECTS": (
        "[]",
        "A JSON list of strings (URLs) to project sites like wikis, GitHub, etc.",
    ),
    "ENABLE_MEMBERBUCKS": (True, "Enable the memberbucks functionality."),
    "MEMBERBUCKS_MAX_TOPUP": ("50", "The maximum topup allowed in dollars."),
    "MEMBERBUCKS_CURRENCY": (
        "aud",
        "The currency to charge cards in - see Stripe documentation.",
    ),
    "ENABLE_THEME_SWIPE": (
        False,
        "Enable playing a member's theme song on a swipe.",
    ),
    "THEME_SWIPE_URL": (
        "http://10.0.1.50/playmp3.php?nickname={}",
        "The URL to send a GET request to on a swipe if enabled.",
    ),
    "ENABLE_DISCORD_INTEGRATION": (
        False,
        "Enable playing a member's theme song on a swipe.",
    ),
    "DISCORD_DOOR_WEBHOOK": (
        "https://discordapp.com/api/webhooks/<token>",
        "Discord URL to send webhook notifications to.",
    ),
    "DISCORD_INTERLOCK_WEBHOOK": (
        "https://discordapp.com/api/webhooks/<token>",
        "Discord URL to send webhook notifications to.",
    ),
    "ENABLE_DISCOURSE_SSO_PROTOCOL": (
        False,
        "Enable support for the discourse SSO protocol.",
    ),
    "DISCOURSE_SSO_PROTOCOL_SECRET_KEY": (
        "",
        "Secret key for the discourse SSO protocol (if enabled).",
    ),
    "GOOGLE_ANALYTICS_PROPERTY_ID": (
        "",
        "Place you google analytics property ID here to enable Google analytics integration.",
    ),
    "API_SECRET_KEY": (
        "PLEASE_CHANGE_ME",
        "The API key used by the internal access system for device authentication.",
    ),
    "SENTRY_DSN_FRONTEND": (
        "https://577dc95136cd402bb273d00f46c2a017@sentry.serv02.binarydigital.com.au/5/",
        "Enter a Sentry DSN to enable sentry logging of frontend errors.",
    ),
    "SENTRY_DSN_BACKEND": (
        "https://8ba460796a9a40d4ac2584e0e8dca59a@sentry.serv02.binarydigital.com.au/4",
        "Enter a Sentry DSN to enable sentry logging of backend errors.",
    ),
    "SENDGRID_API_KEY": (
        "PLEASE_CHANGE_ME",
        "The API key used to send email with Sendgrid.",
    ),
    "INDUCTION_ENROL_LINK": (
        "",
        "The link that a member can use to enrol into an induction.",
    ),
    "INDUCTION_COURSE_ID": (
        "",
        "Canvas course id for the induction.",
    ),
    "MAX_INDUCTION_DAYS": (
        180,
        "The maximum amount of days since a member was last inducted before they have to complete another induction (0 to disable).",
    ),
    "MIN_INDUCTION_SCORE": (
        99,
        "The minimum score to consider an induction as passed (0-100).",
    ),
    "REQUIRE_ACCESS_CARD": (
        True,
        "If an access card is required to be added to a members profile before signup.",
    ),
    "DEFAULT_MEMBER_TYPE": (
        1,
        "The ID of the member type to assign new members to by default.",
    ),
    "CANVAS_API_TOKEN": (
        "PLEASE_CHANGE_ME",
        "Canvas API token.",
    ),
    "ENABLE_PROXY_VOTING": (True, "Enables the proxy voting management feature."),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    [
        (
            "General",
            (
                "SITE_NAME",
                "SITE_OWNER",
                "ENTITY_TYPE",
                "GOOGLE_ANALYTICS_PROPERTY_ID",
                "API_SECRET_KEY",
                "DEFAULT_MEMBER_TYPE",
            ),
        ),
        (
            "Features",
            (
                "ENABLE_PROXY_VOTING",
                "ENABLE_STRIPE_MEMBERSHIP_PAYMENTS",
                "ENABLE_MEMBERBUCKS",
                "ENABLE_DISCOURSE_SSO_PROTOCOL",
                "ENABLE_DISCORD_INTEGRATION",
                "SPACE_DIRECTORY_ENABLED",
                "ENABLE_THEME_SWIPE",
            ),
        ),
        (
            "Sentry Error Reporting",
            (
                "SENTRY_DSN_FRONTEND",
                "SENTRY_DSN_BACKEND",
            ),
        ),
        (
            "Signup",
            (
                "INDUCTION_ENROL_LINK",
                "INDUCTION_COURSE_ID",
                "MAX_INDUCTION_DAYS",
                "MIN_INDUCTION_SCORE",
                "REQUIRE_ACCESS_CARD",
            ),
        ),
        (
            "Canvas Integration",
            ("CANVAS_API_TOKEN",),
        ),
        (
            "Sendgrid Integration",
            ("SENDGRID_API_KEY",),
        ),
        (
            "Contact Information",
            (
                "EMAIL_SYSADMIN",
                "EMAIL_ADMIN",
                "EMAIL_DEFAULT_FROM",
                "SITE_MAIL_ADDRESS",
            ),
        ),
        (
            "Discourse SSO Protocol",
            ("DISCOURSE_SSO_PROTOCOL_SECRET_KEY",),
        ),
        ("URLs", ("SITE_URL", "MAIN_SITE_URL", "CONTACT_PAGE_URL", "INDUCTION_URL")),
        ("Memberbucks", ("MEMBERBUCKS_MAX_TOPUP", "MEMBERBUCKS_CURRENCY")),
        (
            "Images",
            ("SITE_LOGO", "SITE_FAVICON", "STATS_CARD_IMAGE", "MENU_BACKGROUND"),
        ),
        ("Theme", ("THEME_PRIMARY", "THEME_TOOLBAR", "THEME_ACCENT")),
        (
            "Group Localisation",
            (
                "MEMBERBUCKS_NAME",
                "GROUP_NAME",
                "ADMIN_NAME",
                "WEBCAM_PAGE_URLS",
                "HOME_PAGE_CARDS",
                "WELCOME_EMAIL_CARDS",
            ),
        ),
        (
            "Stripe Integration",
            (
                "STRIPE_PUBLISHABLE_KEY",
                "STRIPE_SECRET_KEY",
                "STRIPE_WEBHOOK_SECRET",
                "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS",
            ),
        ),
        (
            "Xero Integration",
            (
                "MAKEMEMBER_CREATE_XERO_INVOICES",
                "STRIPE_CREATE_XERO_INVOICES",
                "XERO_MEMBERBUCKS_ACCOUNT_CODE",
                "XERO_MEMBERSHIP_ACCOUNT_CODE",
                "XERO_MEMBERSHIP_ITEM_CODE",
                "XERO_STRIPE_FEE_ACCOUNT_CODE",
                "XERO_STRIPE_FEE_ITEM_CODE",
                "XERO_TAX_TYPE",
            ),
        ),
        (
            "Trello Integration",
            (
                "ENABLE_TRELLO_INTEGRATION",
                "TRELLO_API_KEY",
                "TRELLO_API_TOKEN",
                "TRELLO_ID_LIST",
            ),
        ),
        (
            "Space Directory",
            (
                "SPACE_DIRECTORY_OPEN",
                "SPACE_DIRECTORY_MESSAGE",
                "SPACE_DIRECTORY_ICON_OPEN",
                "SPACE_DIRECTORY_ICON_CLOSED",
                "SPACE_DIRECTORY_LOCATION_ADDRESS",
                "SPACE_DIRECTORY_LOCATION_LAT",
                "SPACE_DIRECTORY_LOCATION_LON",
                "SPACE_DIRECTORY_FED_SPACENET",
                "SPACE_DIRECTORY_FED_SPACESAML",
                "SPACE_DIRECTORY_CAMS",
                "SPACE_DIRECTORY_CONTACT_EMAIL",
                "SPACE_DIRECTORY_FED_SPACEPHONE",
                "SPACE_DIRECTORY_CONTACT_TWITTER",
                "SPACE_DIRECTORY_CONTACT_FACEBOOK",
                "SPACE_DIRECTORY_CONTACT_PHONE",
                "SPACE_DIRECTORY_PROJECTS",
            ),
        ),
        ("Theme Swipe Integration", ("THEME_SWIPE_URL",)),
        (
            "Discord Integration",
            (
                "DISCORD_DOOR_WEBHOOK",
                "DISCORD_INTERLOCK_WEBHOOK",
            ),
        ),
    ]
)
