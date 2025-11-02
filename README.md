DeepLinks

Turn ESPN+ schedule data into deep-linkable virtual channels and program guides (XMLTV + M3U) that launch streams via a custom URL scheme:

sportscenter://x-callback-url/showWatchStream?playID=<UUID>


Assumes your playback target understands the sportscenter:// scheme (e.g., you have a companion app or handler installed on your streaming device).

What’s in here

espn_scraper.py — pulls ESPN+ schedule into out/espn_schedule.db

generate_guide.py — produces out/espn_plus.xml (XMLTV) and out/espn_plus.m3u (M3U)

hourly.sh — regenerate guide and ask Channels DVR to reload sources

nightly_scrape.sh — refresh the ESPN+ schedule DB nightly

Docs: SUMMARY.md, QUICKSTART_GUIDE.md, GUIDE_GENERATOR_README.md
(Baseline metrics, if present: DEEPLINKS_BASELINE_AUDIT.md)

Prerequisites

Python 3.10+ (tested on Linux)

(Optional) Channels DVR if you want automatic guide reloads

(Optional) A device/app registered to handle sportscenter:// links
(If you use Custom Channels in Channels DVR, STRMLINK is the expected stream format.)

Quick Start

Scrape or refresh the schedule into SQLite:

python3 espn_scraper.py
# writes: out/espn_schedule.db


Generate XMLTV + M3U:

python3 generate_guide.py
# writes: out/espn_plus.xml and out/espn_plus.m3u


Point your consumer (e.g., Channels DVR) at:

XMLTV: out/espn_plus.xml

M3U: out/espn_plus.m3u

Defaults: the scraper loads ~4 days ahead. The guide emits channels for events live now and those starting within ~3 hours, and keeps just-ended events in the set for 65 minutes (the guide shows a 30-min “EVENT ENDED” tile after stop).

Automated Hourly Refresh (recommended)

hourly.sh regenerates the guide and then tells Channels DVR to reload M3U and XMLTV (20-second pause between).

Defaults inside hourly.sh:

HOST: http://127.0.0.1:8089 (override to your Channels host)

M3U_SOURCE: streamlinks

XMLTV_ID: XMLTV-streamlinks

DELAY: 20 seconds

GEN_CMD: python3 generate_guide.py

Run manually:

./hourly.sh


Run hourly via cron (quotes + flock guard):

APP_DIR="<ABSOLUTE_PATH_TO_CLONE>"
mkdir -p "$APP_DIR/logs"
( crontab -l 2>/dev/null | grep -v "$APP_DIR/hourly.sh" ; \
  echo 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' ; \
  echo '0 * * * * /usr/bin/flock -n /tmp/deeplinks_hourly.lock /bin/bash '"$APP_DIR"'/hourly.sh >> '"$APP_DIR"'/logs/hourly.log 2>&1' ) | crontab -

Nightly DB Refresh

Run nightly to keep the DB fresh without hammering upstream:

./nightly_scrape.sh


Cron at 3:30 AM:

APP_DIR="<ABSOLUTE_PATH_TO_CLONE>"
mkdir -p "$APP_DIR/logs"
( crontab -l 2>/dev/null | grep -v "$APP_DIR/nightly_scrape.sh" ; \
  echo 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' ; \
  echo '30 3 * * * /usr/bin/flock -n /tmp/deeplinks_nightly.lock /bin/bash '"$APP_DIR"'/nightly_scrape.sh >> '"$APP_DIR"'/logs/nightly.log 2>&1' ) | crontab -

Conventions

Deep links: sportscenter://x-callback-url/showWatchStream?playID=<UUID>

All times stored as UTC in the DB; display/localization is up to your consumer

“Standby” filler is emitted in 30-min blocks up to ~6h before start (fixed for now)

Roadmap (short)

Parameterize standby/post durations and planning window

Add validation checks (negative durations, explicit gaps, stable channel IDs)

Optional tvg-logo / tvg-chno

Minimal Docker wrapper for scrape + build

CI lint + basic schema regression

Troubleshooting

No channels showing: verify the next 3 hours actually contain events; also check file paths under out/.

Links don’t launch: your device must register a handler for sportscenter://.

Channels DVR reload fails: confirm HOST, M3U_SOURCE, and XMLTV_ID in hourly.sh.

License

MIT — see LICENSE.
