# Quick Start - ESPN+ M3U/XMLTV Guide

## 🎯 What Was Generated

From your **1,141 ESPN+ events**, the generator created:

### Files Created
- **`espn_plus.m3u`** (31 KB) - 129 channels with deep-links
- **`espn_plus.xml`** (122 KB) - Full EPG guide with STAND BY blocks

### Event Breakdown
- **31 LIVE NOW** - Currently in progress
- **98 UPCOMING** - Starting within next 3 hours
- **129 Total Channels** - One per event

## 🚀 Quick Usage

### 1. Generate the Files

```bash
python generate_guide.py /path/to/espn_schedule.db
```

### 2. Use the M3U

**Sample M3U entry:**
```m3u
#EXTINF:-1 tvg-id="espnplus1" tvg-name="ESPN+ 1: College GameDay" group-title="ESPN+"
sportscenter://x-callback-url/showWatchStream?playID=050a7ede-f239-47ea-87ff-fbd0dcd0ecd4
```

### 3. View the EPG

The XML includes:
- **STAND BY blocks** before events (30-min increments, up to 6 hours)
- **The actual event** with sport/league metadata
- **EVENT ENDED blocks** after events (30 minutes)

## 📺 Example Guide Timeline

```
Channel: ESPN+ 52 - Hurricanes vs. Bruins
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15:50 - 16:20  │ STAND BY (Event starts at 16:30)
16:20 - 16:30  │ STAND BY (Event starts at 16:30)  
16:30 - 20:30  │ 🏒 Hurricanes vs. Bruins (LIVE)
20:30 - 21:00  │ EVENT ENDED
```

## 🔗 Deep Link Format

```
sportscenter://x-callback-url/showWatchStream?playID=<UUID>
```

- **Scheme**: `sportscenter://` (opens ESPN app)
- **playID**: 36-character UUID from database
- **No encoding needed** - use UUID as-is

## 📊 Sample Channels

From the generated playlist:

1. **ESPN+ 1**: College GameDay (NCAA Football) - LIVE
2. **ESPN+ 4**: A10 Cross Country Championship - LIVE
3. **ESPN+ 7**: Marshall vs. James Madison - LIVE
4. **ESPN+ 52**: Hurricanes vs. Bruins - 16:30 UTC
5. **ESPN+ 54**: #14 Kansas vs. West Virginia - 17:00 UTC

## 🔄 Workflow

```
┌─────────────────┐
│ espn_scraper.py │──► Fetch ESPN+ events
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ espn_schedule.db│──► 1,141 events stored
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│generate_guide.py│──► Filter live + upcoming
└────────┬────────┘
         │
         ├──► espn_plus.m3u  (129 channels)
         └──► espn_plus.xml  (EPG with STAND BY)
```

## 🎮 Using the Deep Links

### On iOS/iPadOS
```
Open: sportscenter://x-callback-url/showWatchStream?playID=...
→ Opens ESPN app directly to stream
```

### On Android
```
Intent: sportscenter://x-callback-url/showWatchStream?playID=...
→ Launches ESPN app to player
```

### On Web/Desktop
Deep links work best with ESPN app installed. For web viewing, the database also includes `web_url` field with standard HTTPS links.

## ⚙️ Customization

### Change Time Window

Edit `generate_guide.py` line ~282:
```python
events = get_live_and_upcoming_events(db_path, hours_ahead=3)
# Change to:
events = get_live_and_upcoming_events(db_path, hours_ahead=6)
```

### Adjust STAND BY Duration

Edit configuration at top of script:
```python
STANDBY_BLOCK_DURATION_MIN = 30  # Change to 60 for 1-hour blocks
MAX_STANDBY_HOURS = 6            # Change to 12 for longer standby
```

### Filter by Sport

Modify the SQL query (line ~29):
```python
query = """
    SELECT * FROM events
    WHERE datetime(stop_utc) > datetime('now')
      AND datetime(start_utc) <= datetime('now', '+3 hours')
      AND sport = 'Basketball'  -- Add this filter
    ORDER BY start_utc, title
"""
```

## 📱 IPTV Player Setup

### TiviMate
1. Add Playlist → External M3U
2. Playlist URL: `file:///path/to/espn_plus.m3u`
3. EPG Source → XMLTV
4. EPG URL: `file:///path/to/espn_plus.xml`

### IPTV Smarters
1. Add New User → Load M3U
2. M3U File/URL: Select `espn_plus.m3u`
3. EPG URL: Select `espn_plus.xml`

### Perfect Player
1. Settings → General → Playlists
2. Add playlist → `espn_plus.m3u`
3. Settings → EPG → XMLTV source
4. Add source → `espn_plus.xml`

## 🔧 Automation

### Update Every Hour

**Bash script:**
```bash
#!/bin/bash
cd /path/to/project
python3 espn_scraper.py          # Refresh database
python3 generate_guide.py         # Generate M3U/XML
# Optional: upload to web server
# scp espn_plus.* user@server:/var/www/html/
```

**Cron job:**
```bash
0 * * * * /path/to/update_espn.sh
```

## 📈 Stats from Generated Files

- **M3U**: 129 channels, 258 lines, 31 KB
- **XMLTV**: 2,538 lines, 122 KB
- **Programmes**: ~390 (including STAND BY + EVENT ENDED blocks)
- **Sports Covered**: Football, Basketball, Hockey, Soccer, etc.

## 🎯 Next Steps

1. **Test the M3U** in your IPTV player
2. **Verify deep links** work on your device
3. **Set up automation** to refresh hourly
4. **Customize filters** for your favorite sports
5. **Serve via HTTP** for remote access

## 📚 Documentation

- **Full Guide**: See `GUIDE_GENERATOR_README.md`
- **Script**: `generate_guide.py`
- **Database Tool**: `query_espn.py`

---

**Generated**: 2025-11-01 15:50:33 UTC
**Events**: 129 (31 live, 98 upcoming)
**Time Window**: 3 hours ahead
