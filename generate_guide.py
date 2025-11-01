#!/usr/bin/env python3
"""
ESPN+ M3U and XMLTV Generator
Generates playlists and guide for live and upcoming events
"""

import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree as ET
from xml.dom import minidom
import os

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "out", "espn_schedule.db")
M3U_OUTPUT = "espn_plus.m3u"
XML_OUTPUT = "espn_plus.xml"

STANDBY_BLOCK_DURATION_MIN = 30  # 30 minute standby blocks
MAX_STANDBY_HOURS = 6             # Max 6 hours of standby before event
EVENT_ENDED_DURATION_MIN = 30     # 30 minute "event ended" block

def get_live_and_upcoming_events(db_path, hours_ahead=3):
    """
    Get events that are either:
    - Live now (started but not ended)
    - Starting within next N hours
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(hours=hours_ahead)
    
    # Query for events that:
    # 1. Haven't ended yet (stop_utc > now)
    # 2. Either already started (start_utc <= now) OR starting soon (start_utc <= window_end)
    query = """
        SELECT * FROM events
        WHERE datetime(stop_utc) > datetime('now')
          AND datetime(start_utc) <= datetime('now', '+{} hours')
        ORDER BY start_utc, title
    """.format(hours_ahead)
    
    cursor = conn.execute(query)
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return events

def parse_iso_datetime(dt_str):
    """Parse ISO8601 datetime string to timezone-aware datetime"""
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    return datetime.fromisoformat(dt_str)

def format_datetime_xmltv(dt):
    """Format datetime for XMLTV format: YYYYMMDDHHmmss +0000"""
    return dt.strftime('%Y%m%d%H%M%S +0000')

def extract_play_id(event):
    """Extract play ID from event (the UUID)"""
    # The ID field is the UUID we need
    return event['id']

def build_deep_link(play_id):
    """Build the ESPN deep link URL"""
    return f"sportscenter://x-callback-url/showWatchStream?playID={play_id}"

def generate_m3u(events):
    """Generate M3U playlist"""
    lines = ['#EXTM3U']
    
    # Create a channel for each event
    for idx, event in enumerate(events, 1):
        channel_num = idx
        play_id = extract_play_id(event)
        deep_link = build_deep_link(play_id)
        
        # Event info
        title = event.get('title', 'Unknown Event')
        sport = event.get('sport', '')
        league = event.get('league', '')
        
        # Build channel name
        channel_name = f"ESPN+ {channel_num}: {title}"
        if league:
            channel_name += f" ({league})"
        
        # Add to M3U
        lines.append(f'#EXTINF:-1 tvg-id="espnplus{channel_num}" tvg-name="{channel_name}" tvg-logo="" group-title="ESPN+",{channel_name}')
        lines.append(deep_link)
    
    return '\n'.join(lines)

def generate_standby_blocks(channel_id, start_time, now):
    """
    Generate STAND BY placeholder blocks before an event starts.
    Creates 30-minute blocks from now until event start (max 6 hours).
    """
    blocks = []
    
    # Calculate how much time until event starts
    time_until = (start_time - now).total_seconds() / 60  # minutes
    
    if time_until <= 0:
        return []  # Event already started or starting now
    
    # Cap at MAX_STANDBY_HOURS
    max_standby_min = MAX_STANDBY_HOURS * 60
    standby_duration = min(time_until, max_standby_min)
    
    # Create 30-minute blocks
    current_time = now
    blocks_needed = int(standby_duration / STANDBY_BLOCK_DURATION_MIN)
    
    for i in range(blocks_needed):
        block_start = current_time
        block_stop = current_time + timedelta(minutes=STANDBY_BLOCK_DURATION_MIN)
        
        # Don't go past the event start time
        if block_stop > start_time:
            block_stop = start_time
        
        blocks.append({
            'start': format_datetime_xmltv(block_start),
            'stop': format_datetime_xmltv(block_stop),
            'title': 'STAND BY',
            'desc': f'Event starts at {start_time.strftime("%H:%M UTC")}'
        })
        
        current_time = block_stop
        
        if current_time >= start_time:
            break
    
    return blocks

def generate_event_ended_block(channel_id, end_time):
    """Generate EVENT ENDED block after event finishes"""
    block_start = end_time
    block_stop = end_time + timedelta(minutes=EVENT_ENDED_DURATION_MIN)
    
    return {
        'start': format_datetime_xmltv(block_start),
        'stop': format_datetime_xmltv(block_stop),
        'title': 'EVENT ENDED',
        'desc': 'This event has concluded'
    }

def generate_xmltv(events):
    """Generate XMLTV guide"""
    now = datetime.now(timezone.utc)
    
    # Create root element
    tv = ET.Element('tv')
    tv.set('generator-info-name', 'ESPN+ Guide Generator')
    tv.set('generator-info-url', 'https://github.com/yourusername/espn-guide')
    
    # Add channels
    for idx, event in enumerate(events, 1):
        channel_id = f"espnplus{idx}"
        
        channel = ET.SubElement(tv, 'channel')
        channel.set('id', channel_id)
        
        display_name = ET.SubElement(channel, 'display-name')
        title = event.get('title', 'Unknown Event')
        league = event.get('league', '')
        display_name.text = f"ESPN+ {idx}: {title}" + (f" ({league})" if league else "")
    
    # Add programmes for each channel
    for idx, event in enumerate(events, 1):
        channel_id = f"espnplus{idx}"
        
        start_time = parse_iso_datetime(event['start_utc'])
        stop_time = parse_iso_datetime(event['stop_utc'])
        
        # Determine if event has started
        is_live = start_time <= now < stop_time
        is_upcoming = start_time > now
        
        # Generate STAND BY blocks if event hasn't started
        if is_upcoming:
            standby_blocks = generate_standby_blocks(channel_id, start_time, now)
            for block in standby_blocks:
                programme = ET.SubElement(tv, 'programme')
                programme.set('start', block['start'])
                programme.set('stop', block['stop'])
                programme.set('channel', channel_id)
                
                title_elem = ET.SubElement(programme, 'title')
                title_elem.set('lang', 'en')
                title_elem.text = block['title']
                
                desc_elem = ET.SubElement(programme, 'desc')
                desc_elem.set('lang', 'en')
                desc_elem.text = block['desc']
        
        # Add the actual event
        programme = ET.SubElement(tv, 'programme')
        programme.set('start', format_datetime_xmltv(start_time))
        programme.set('stop', format_datetime_xmltv(stop_time))
        programme.set('channel', channel_id)
        
        # Add LIVE tag if event is currently live (XMLTV standard)
        if is_live:
            live = ET.SubElement(programme, 'live')
        
        # Title
        title_elem = ET.SubElement(programme, 'title')
        title_elem.set('lang', 'en')
        title_elem.text = event.get('title', 'Unknown Event')
        
        # Subtitle (network/league)
        if event.get('subtitle') or event.get('league'):
            subtitle_elem = ET.SubElement(programme, 'sub-title')
            subtitle_elem.set('lang', 'en')
            subtitle_text = event.get('subtitle') or event.get('league')
            subtitle_elem.text = subtitle_text
        
        # Description
        desc_elem = ET.SubElement(programme, 'desc')
        desc_elem.set('lang', 'en')
        sport = event.get('sport', '')
        league = event.get('league', '')
        desc_parts = []
        if sport:
            desc_parts.append(f"Sport: {sport}")
        if league:
            desc_parts.append(f"League: {league}")
        desc_parts.append(f"Status: {'LIVE NOW' if is_live else 'Upcoming'}")
        desc_elem.text = ' | '.join(desc_parts)
        
        # Categories - Add both SPORTS and SPORTS EVENT
        category_sports = ET.SubElement(programme, 'category')
        category_sports.set('lang', 'en')
        category_sports.text = 'SPORTS'
        
        category_event = ET.SubElement(programme, 'category')
        category_event.set('lang', 'en')
        category_event.text = 'SPORTS EVENT'
        
        # Add specific sport category if available
        if sport:
            category = ET.SubElement(programme, 'category')
            category.set('lang', 'en')
            category.text = sport
        
        # Add EVENT ENDED block after event
        ended_block = generate_event_ended_block(channel_id, stop_time)
        programme = ET.SubElement(tv, 'programme')
        programme.set('start', ended_block['start'])
        programme.set('stop', ended_block['stop'])
        programme.set('channel', channel_id)
        
        title_elem = ET.SubElement(programme, 'title')
        title_elem.set('lang', 'en')
        title_elem.text = ended_block['title']
        
        desc_elem = ET.SubElement(programme, 'desc')
        desc_elem.set('lang', 'en')
        desc_elem.text = ended_block['desc']
    
    # Pretty print XML
    xml_str = ET.tostring(tv, encoding='unicode')
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent='  ')

def main():
    # Allow custom database path
    db_path = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        sys.exit(1)
    
    print("ESPN+ M3U/XMLTV Generator")
    print("=" * 60)
    print(f"Database: {db_path}")
    print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    # Get events
    print("Fetching live and upcoming events (next 3 hours)...")
    events = get_live_and_upcoming_events(db_path, hours_ahead=3)
    
    if not events:
        print("No live or upcoming events found!")
        sys.exit(0)
    
    print(f"Found {len(events)} events")
    print()
    
    # Show summary
    now = datetime.now(timezone.utc)
    live_count = sum(1 for e in events if parse_iso_datetime(e['start_utc']) <= now < parse_iso_datetime(e['stop_utc']))
    upcoming_count = len(events) - live_count
    
    print(f"  Live now: {live_count}")
    print(f"  Upcoming: {upcoming_count}")
    print()
    
    # Generate M3U
    print("Generating M3U playlist...")
    m3u_content = generate_m3u(events)
    
    with open(M3U_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    
    print(f"  Saved: {M3U_OUTPUT}")
    print(f"  Channels: {len(events)}")
    print()
    
    # Generate XMLTV
    print("Generating XMLTV guide...")
    xml_content = generate_xmltv(events)
    
    with open(XML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"  Saved: {XML_OUTPUT}")
    print()
    
    # Show sample events
    print("Sample events:")
    print("-" * 60)
    for i, event in enumerate(events[:5], 1):
        title = event.get('title', 'Unknown')
        start = parse_iso_datetime(event['start_utc'])
        is_live = start <= now < parse_iso_datetime(event['stop_utc'])
        status = "🔴 LIVE" if is_live else f"⏰ {start.strftime('%H:%M UTC')}"
        print(f"{i}. {status} - {title}")
    
    if len(events) > 5:
        print(f"... and {len(events) - 5} more")
    
    print()
    print("=" * 60)
    print("✓ Generation complete!")
    print()
    print("Files created:")
    print(f"  M3U:  {M3U_OUTPUT}")
    print(f"  XMLTV: {XML_OUTPUT}")

if __name__ == "__main__":
    main()
