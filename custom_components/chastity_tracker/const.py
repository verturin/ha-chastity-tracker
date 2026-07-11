"""Constants for the Chastity Tracker integration."""

DOMAIN = "chastity_tracker"

CONF_BASE_URL = "base_url"
CONF_API_TOKEN = "api_token"
CONF_USE_APP_PHP = "use_app_php"

DEFAULT_BASE_URL = "https://cage-et-chastete.com"
DEFAULT_SCAN_INTERVAL = 300  # secondes
DEFAULT_USE_APP_PHP = True

API_PATH = "/chastity/api"
APP_PHP_PREFIX = "/app.php"

ATTR_STATUS = "status"
ATTR_LOCKED = "locked"
ATTR_DAYS_CURRENT = "days_current"
ATTR_DAYS_SINCE_LAST = "days_since_last"
ATTR_TOTAL_DAYS = "total_days"
ATTR_DAYS_CURRENT_YEAR = "days_current_year"
ATTR_TAGLINE = "tagline"
ATTR_ALIAS = "alias"
ATTR_HIDE_STATUS = "hide_status"
ATTR_IS_KEYHOLDER = "is_keyholder"
ATTR_HAS_ACTIVE_KH = "has_active_kh"
ATTR_HAS_ACTIVE_CONTRACT = "has_active_contract"
ATTR_KH_SUBS_COUNT = "kh_subs_count"
ATTR_GENDER = "gender"
ATTR_KEYHOLDER_LABEL = "keyholder_label"
