# ESPN+ M3U/XMLTV Generator - Complete Package

## ✅ What You Have

### 🎬 Generated Files (from your database)

**[espn_plus.m3u](computer:///mnt/user-data/outputs/espn_plus.m3u)** (31 KB)
- 129 ESPN+ channels with deep-links
- Format: `sportscenter://x-callback-url/showWatchStream?playID=<UUID>`
- Ready for IPTV players

**[espn_plus.xml](computer:///mnt/user-data/outputs/espn_plus.xml)** (122 KB)
- Complete XMLTV EPG guide
- STAND BY blocks before events (up to 6 hours)
- EVENT ENDED blocks after events
- 2,538 programme entries

### 🛠️ Tools

**[generate_guide.py](computer:///mnt/user-data/outputs/generate_guide.py)** (11 KB)
- Main generator script
- Filters live + upcoming events (3 hour window)
- Creates M3U playlist and XMLTV guide
- Configurable time windows and block durations

### 📚 Documentation

**[GUIDE_GENERATOR_README.md](computer:///mnt/user-data/outputs/GUIDE_GENERATOR_README.md)** (7.5 KB)
- Complete reference guide
- Configuration options
- IPTV player setup
- Automation examples

**[QUICKSTART_GUIDE.md](computer:///mnt/user-data/outputs/QUICKSTART_GUIDE.md)** (5.3 KB)
- Quick start instructions
- Sample output
- Usage examples
- Stats from your generated files

## 📊 Your Generated Guide Stats

From your database of **1,141 ESPN+ events**:

```
┌──────────────────────────────────────┐
│  ESPN+ Live & Upcoming Events        │
├──────────────────────────────────────┤
│  🔴 Live Now:           31 events    │
│  ⏰ Upcoming (3h):      98 events    │
│  📺 Total Channels:    129 channels  │
│  📅 Time Window:        3 hours      │
└──────────────────────────────────────┘
```

## 🎯 Key Features

✅ **Deep-Link URLs**: Uses `sportscenter://` for direct ESPN app playback
✅ **Live Detection**: Automatically identifies currently streaming events
✅ **Smart Scheduling**: STAND BY blocks fill time before events
✅ **Multi-Sport**: Basketball, Football, Hockey, Soccer, and more
✅ **EPG Ready**: Full XMLTV guide with programme metadata

## 🚀 Quick Usage

```bash
# Generate M3U + XMLTV from your database
python generate_guide.py /path/to/espn_schedule.db

# Output:
#   espn_plus.m3u  - Playlist with 129 channels
#   espn_plus.xml  - EPG guide with timing blocks
```

## 📺 Sample Channels

Your generated playlist includes:

1. **ESPN+ 1**: College GameDay (NCAA Football) 🔴 LIVE
2. **ESPN+ 4**: A10 Cross Country Championship 🔴 LIVE
3. **ESPN+ 7**: Marshall vs. James Madison 🔴 LIVE
4. **ESPN+ 10**: Heidenheim vs. Frankfurt 🔴 LIVE
5. **ESPN+ 52**: Hurricanes vs. Bruins ⏰ 16:30 UTC
6. **ESPN+ 54**: #14 Kansas vs. West Virginia ⏰ 17:00 UTC

## 🔗 Deep Link Format

Each channel uses ESPN's deep-link format:

```
sportscenter://x-callback-url/showWatchStream?playID=050a7ede-f239-47ea-87ff-fbd0dcd0ecd4
```

**Benefits**:
- Direct launch to ESPN app
- No web navigation needed
- Works on iOS, Android, and supported platforms

## 📋 EPG Guide Structure

```
Channel Timeline Example:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15:50 │ STAND BY - Event starts at 16:30 UTC
16:20 │ STAND BY - Event starts at 16:30 UTC
16:30 │ 🏒 Hurricanes vs. Bruins (LIVE)
20:30 │ EVENT ENDED - This event has concluded
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🎮 Using with IPTV Players

### TiviMate (Android)
1. Settings → Playlists → Add Playlist
2. Choose M3U File: `espn_plus.m3u`
3. Settings → EPG → Add EPG source
4. Choose XML file: `espn_plus.xml`

### IPTV Smarters
1. Add User → Load M3U
2. Select `espn_plus.m3u`
3. Add EPG URL → Select `espn_plus.xml`

### VLC
```bash
vlc espn_plus.m3u
```

### Plex / Jellyfin / Channels DVR
- Add M3U as tuner source
- Add XMLTV as EPG source

## 🔄 Automation

### Update Every Hour

**Linux/Mac**:
```bash
# Add to crontab
0 * * * * cd /path/to/project && python3 generate_guide.py
```

**Windows**:
- Task Scheduler → Create Task
- Trigger: Hourly
- Action: Run `python generate_guide.py`

### Serve via HTTP

```bash
python3 -m http.server 8080
# Access at: http://localhost:8080/espn_plus.m3u
```

## 🎨 Customization

### Change Time Window
```python
# In generate_guide.py, line ~282
hours_ahead=3  # Change to 6 for 6-hour window
```

### Adjust STAND BY Blocks
```python
STANDBY_BLOCK_DURATION_MIN = 30  # 30-min blocks
MAX_STANDBY_HOURS = 6            # Max 6 hours before event
EVENT_ENDED_DURATION_MIN = 30    # 30-min after event
```

### Filter by Sport
```python
# In SQL query, add:
AND sport = 'Basketball'  # Only basketball
```

## 📁 Complete File List

```
ESPN+ Guide Generator Package:
├── generate_guide.py              Main generator script
├── espn_plus.m3u                  M3U playlist (129 channels)
├── espn_plus.xml                  XMLTV guide (2,538 entries)
├── GUIDE_GENERATOR_README.md      Full documentation
├── QUICKSTART_GUIDE.md            Quick start guide
└── SUMMARY.md                     This file
```

## 🔗 Related Tools

- **espn_scraper.py**: Fetches events from ESPN API
- **query_espn.py**: Query and explore the database
- **espn_schedule.db**: Your 1,141 event database

## 🎯 Next Steps

1. ✅ **Generated** - M3U and XMLTV files created
2. ⏭️ **Test** - Try in your IPTV player
3. ⏭️ **Automate** - Set up hourly refresh
4. ⏭️ **Customize** - Adjust filters and time windows
5. ⏭️ **Deploy** - Serve via HTTP for remote access

## 💡 Tips

- **Refresh frequently**: Run generator every hour for latest events
- **Check deep links**: Ensure ESPN app is installed on device
- **Monitor logs**: Watch for API changes or errors
- **Backup database**: Keep copies of espn_schedule.db
- **Test first**: Verify a few channels work before full deployment

## 📝 Notes

- Deep links work best with ESPN app installed
- STAND BY blocks ensure smooth EPG display
- Times are in UTC (convert for local viewing)
- Database needs periodic refresh from scraper
- Respects ESPN's Terms of Service

---

**Package Generated**: 2025-11-01 15:50:33 UTC
**Total Channels**: 129
**Live Events**: 31
**Upcoming Events**: 98
**Database Size**: 1,141 ESPN+ events
