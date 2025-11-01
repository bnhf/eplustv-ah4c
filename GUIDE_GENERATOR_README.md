# ESPN+ M3U/XMLTV Guide Generator

Generates M3U playlists and XMLTV guides for live and upcoming ESPN+ events with deep-link support.

## 🎯 Features

- ✅ **Live Events**: Includes events currently in progress
- ✅ **Upcoming Events**: Shows events starting within next 3 hours
- ✅ **Deep Links**: Uses `sportscenter://` URL scheme for direct playback
- ✅ **STAND BY Blocks**: Adds placeholder programmes before events start (up to 6 hours)
- ✅ **EVENT ENDED Blocks**: Shows 30-minute blocks after events finish
- ✅ **Multi-Channel**: Creates separate channel for each event

## 📋 Requirements

- Python 3.7+
- SQLite3 database from `espn_scraper.py`

## 🚀 Usage

### Basic Usage

```bash
python generate_guide.py
```

Uses default database path: `../out/espn_schedule.db`

### Custom Database Path

```bash
python generate_guide.py /path/to/espn_schedule.db
```

## 📁 Output Files

### M3U Playlist (`espn_plus.m3u`)

```m3u
#EXTM3U
#EXTINF:-1 tvg-id="espnplus1" tvg-name="ESPN+ 1: Event Name" group-title="ESPN+",ESPN+ 1: Event Name
sportscenter://x-callback-url/showWatchStream?playID=918d253f-7a02-4fb0-b130-8aa06237611c
```

**Format:**
- One channel per event
- Deep-link URL using ESPN's `sportscenter://` scheme
- `playID` parameter contains the ESPN Watch UUID

### XMLTV Guide (`espn_plus.xml`)

```xml
<tv>
  <channel id="espnplus1">
    <display-name>ESPN+ 1: Event Name</display-name>
  </channel>
  
  <programme start="20251101150000 +0000" stop="20251101153000 +0000" channel="espnplus1">
    <title lang="en">STAND BY</title>
    <desc lang="en">Event starts at 16:00 UTC</desc>
  </programme>
  
  <programme start="20251101160000 +0000" stop="20251101180000 +0000" channel="espnplus1">
    <title lang="en">Event Name</title>
    <sub-title lang="en">NETWORK</sub-title>
    <desc lang="en">Sport: Basketball | League: NBA | Status: LIVE NOW</desc>
    <category lang="en">Basketball</category>
  </programme>
  
  <programme start="20251101180000 +0000" stop="20251101183000 +0000" channel="espnplus1">
    <title lang="en">EVENT ENDED</title>
    <desc lang="en">This event has concluded</desc>
  </programme>
</tv>
```

**Programme Types:**
1. **STAND BY**: 30-minute blocks before event starts (max 6 hours)
2. **Event**: The actual sporting event with metadata
3. **EVENT ENDED**: 30-minute block after event finishes

## 🎮 Deep Link Format

The generator uses ESPN's deep-link URL scheme:

```
sportscenter://x-callback-url/showWatchStream?playID=<UUID>
```

**Components:**
- **Scheme**: `sportscenter://`
- **Path**: `/x-callback-url/showWatchStream`
- **Parameter**: `playID=<36-char UUID>`

**Example:**
```
sportscenter://x-callback-url/showWatchStream?playID=918d253f-7a02-4fb0-b130-8aa06237611c
```

This launches the ESPN app directly to the stream player.

## ⏰ Time Windows

### Live Events
Events are considered "live" if:
- `start_utc` <= current time
- `stop_utc` > current time

### Upcoming Events
Events are included if:
- `start_utc` <= (current time + 3 hours)
- `stop_utc` > current time

## 📊 Example Output

```
ESPN+ M3U/XMLTV Generator
============================================================
Database: ../out/espn_schedule.db
Time: 2025-11-01 15:50:33 UTC

Fetching live and upcoming events (next 3 hours)...
Found 129 events

  Live now: 31
  Upcoming: 98

Generating M3U playlist...
  Saved: espn_plus.m3u
  Channels: 129

Generating XMLTV guide...
  Saved: espn_plus.xml

Sample events:
------------------------------------------------------------
1. 🔴 LIVE - College GameDay Built by The Home Depot
2. 🔴 LIVE - A10 Cross Country Championship
3. 🔴 LIVE - ACC Huddle
4. ⏰ 16:30 UTC - Hurricanes vs. Bruins
5. ⏰ 17:00 UTC - #14 Kansas vs. West Virginia
... and 124 more

============================================================
✓ Generation complete!

Files created:
  M3U:  espn_plus.m3u
  XMLTV: espn_plus.xml
```

## 🔧 Configuration

Edit the script to customize:

```python
# Time window for upcoming events
hours_ahead=3  # Change to 6 for 6-hour window

# STAND BY block duration
STANDBY_BLOCK_DURATION_MIN = 30  # 30 minutes per block

# Maximum standby time before event
MAX_STANDBY_HOURS = 6  # Max 6 hours of standby blocks

# EVENT ENDED block duration
EVENT_ENDED_DURATION_MIN = 30  # 30 minutes
```

## 📺 Using with IPTV Players

### VLC

```bash
vlc espn_plus.m3u
```

**Note**: VLC may not support the `sportscenter://` URL scheme. Consider using on devices with ESPN app installed.

### TiviMate (Android)

1. Add M3U playlist URL
2. Add XMLTV URL for EPG
3. Enable EPG sync

### Channels DVR

1. Add as Custom Channel
2. Point to M3U URL
3. Add XMLTV as EPG source

### IPTV Smarters

1. Go to Add Playlist
2. Select "M3U URL" or "File"
3. Add EPG source with XML URL

## 🔄 Automation

### Run Every Hour

**Linux/Mac (cron):**
```bash
# Edit crontab
crontab -e

# Add line to run every hour
0 * * * * cd /path/to/project && python3 generate_guide.py
```

**Windows (Task Scheduler):**
1. Create Basic Task
2. Trigger: Every 1 hour
3. Action: Start Program
4. Program: `python.exe`
5. Arguments: `C:\path\to\generate_guide.py`

### Serve Files via HTTP

```bash
# Simple HTTP server
cd /path/to/output
python3 -m http.server 8080

# Access files at:
# http://localhost:8080/espn_plus.m3u
# http://localhost:8080/espn_plus.xml
```

## 🎨 Channel Naming

Channels are named: `ESPN+ <NUM>: <EVENT TITLE> (<LEAGUE>)`

**Examples:**
- `ESPN+ 1: Hurricanes vs. Bruins (NHL)`
- `ESPN+ 2: #10 Miami vs. SMU (NCAA Football)`
- `ESPN+ 3: Bundesliga Goal Arena`

## 📝 Programme Details

Each event programme includes:
- **Title**: Event name
- **Sub-title**: Network or league
- **Description**: Sport, league, and status
- **Category**: Sport type
- **Time**: Start/stop in XMLTV format

**STAND BY blocks** show:
- Title: "STAND BY"
- Description: "Event starts at HH:MM UTC"

**EVENT ENDED blocks** show:
- Title: "EVENT ENDED"
- Description: "This event has concluded"

## 🐛 Troubleshooting

### No events found
```
No live or upcoming events found!
```
**Solution**: 
- Check if database has recent data
- Run `espn_scraper.py` to refresh
- Verify events exist in next 3 hours

### Database not found
```
Error: Database not found at ../out/espn_schedule.db
```
**Solution**: 
- Run `espn_scraper.py` first
- Or specify custom path: `python generate_guide.py /path/to/db`

### Empty M3U/XML
**Solution**:
- Check database has ESPN+ events (`is_plus = 1`)
- Verify events haven't expired
- Check event times are in correct format

## 🔗 Integration Examples

### Home Assistant

```yaml
# configuration.yaml
iptv:
  channels:
    - name: ESPN+ Live
      url: http://your-server:8080/espn_plus.m3u
  epg:
    - url: http://your-server:8080/espn_plus.xml
```

### Plex Live TV

1. Settings → Live TV & DVR
2. Add a Device
3. Select DVR
4. Add M3U URL
5. Add EPG XML URL

### Jellyfin

1. Dashboard → Live TV
2. Add Tuner Device
3. Type: M3U Tuner
4. File or URL: `/path/to/espn_plus.m3u`
5. Add EPG: `/path/to/espn_plus.xml`

## 📚 Related Scripts

- **`espn_scraper.py`**: Fetches events from ESPN API
- **`query_espn.py`**: Query and explore the database

## 🎯 Tips

1. **Refresh frequently**: Run every hour to catch new events
2. **Filter by sport**: Modify SQL query to filter specific sports
3. **Custom time window**: Adjust `hours_ahead` parameter
4. **Deep link compatibility**: Works best with ESPN app installed
5. **EPG sync**: Set IPTV player to refresh EPG hourly

## 📄 License

Educational use only. Respect ESPN's Terms of Service.
