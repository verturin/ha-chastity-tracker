"""Constants for the Chastity Tracker integration."""

DOMAIN = "chastity_tracker"

CONF_BASE_URL = "base_url"
CONF_API_TOKEN = "api_token"

DEFAULT_BASE_URL = "https://cage-et-chastete.com"
DEFAULT_SCAN_INTERVAL = 300  # secondes

API_PATH = "/chastity/api"

ATTR_STATUS = "status"
ATTR_LOCKED = "locked"
ATTR_DAYS_CURRENT = "days_current"
ATTR_DAYS_SINCE_LAST = "days_since_last"
ATTR_TOTAL_DAYS = "total_days"
ATTR_DAYS_CURRENT_YEAR = "days_current_year"
ATTR_TAGLINE = "tagline"
