DEFAULT_URLS = [
    "https://robocup-ssl.github.io/ssl-goals/sslgoals.html",
    "https://robocup-ssl.github.io/ssl-rules/sslrules.html",
    "https://github.com/orgs/RoboCup-SSL/repositories",
    "https://ssl.robocup.org/rules/",
    "https://ssl.robocup.org/tournament-rules/",
    "https://ssl.robocup.org/technical-overview-of-the-small-size-league/",
    "https://ssl.robocup.org/tournament-organization/",
    "https://ssl.robocup.org/divisions/",
    "https://ssl.robocup.org/open-source-contributions/",
    "https://ssl.robocup.org/history-of-open-source-submissions/",
    "https://ssl.robocup.org/scientific-publications/",
    "https://ssl.robocup.org/team-description-papers/",
    "https://ssl.robocup.org/history-of-technical-challenges/",
    "https://ssl.robocup.org/match-statistics/",
    "https://ssl.robocup.org/contact/",
]

# Keywords to filter out from URLs
URL_BLACKLIST = [
    "comittee",
    "comittees",
    "qualification",
    "teams",
    "results",
]

# Sitemap URL
DEFAULT_SITEMAP_URL = "https://ssl.robocup.org/page-sitemap.html"

# Output file for processed URLs
URLS_FILE_PATH = "data/processed_urls.txt"

# Full website file path
FULL_WEBSITE_FILE_PATH = "data/full_website.txt"

# Vector store path
VECTOR_STORE_PATH = "data/"

# Vector store collection name
VECTOR_STORE_COLLECTION_NAME = "small-size-league-mcp"
