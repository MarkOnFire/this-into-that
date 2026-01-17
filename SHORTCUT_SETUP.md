# Apple Music Playlist Creator Shortcut

This guide helps you create a macOS Shortcut that takes the output from This Into That and creates an Apple Music playlist.

## One-Time Setup (5 minutes)

### Step 1: Open Shortcuts App
```bash
open -a Shortcuts
```

### Step 2: Create New Shortcut
1. Click **+** to create a new shortcut
2. Name it: `Import to Apple Music Playlist`

### Step 3: Add These Actions (in order)

**Action 1: Receive Input**
- Search for "Receive" → Add "Receive **any** input from **Shortcuts**"
- Set to: "If there's no input: **Ask for Input**"

**Action 2: Split Text**
- Search for "Split" → Add "Split Text"
- Split by: **New Lines**

**Action 3: Repeat with Each**
- Search for "Repeat" → Add "Repeat with Each"
- Repeat with each item in: **Split Text**

**Inside the Repeat block, add:**

**Action 4: Search Apple Music**
- Search for "Search" → Add "Search Apple Music"
- Search for: **Repeat Item**
- This searches the Apple Music catalog (not just your library)

**Action 5: Get First Item**
- Search for "Get Item" → Add "Get Item from List"
- Get: **First Item** from **Music**

**Action 6: Add to Playlist**
- Search for "Add to" → Add "Add to Playlist"
- Add: **Item from List** to: **(select your target playlist or "Ask Each Time")**

**End Repeat** (this happens automatically)

### Step 4: Save the Shortcut
- Click **Done** or Cmd+S

## Usage

### From This Into That:
The tool outputs a file with one "Artist - Song Title" per line. Run:

```bash
cat songs_for_playlist.txt | shortcuts run "Import to Apple Music Playlist"
```

### From Command Line:
```bash
echo "Creedence Clearwater Revival - Fortunate Son
Bob Dylan - Blowin' in the Wind
Linkin Park - Numb" | shortcuts run "Import to Apple Music Playlist"
```

## Alternative: Quick Manual Add

If the Shortcut approach doesn't work well, use the markdown file:
1. Open `political_songs_apple_music.md` in a markdown viewer
2. Cmd+Click each `music://` link to open in Music.app
3. Press Cmd+Shift+N to add to a new playlist

## Troubleshooting

**"Search Apple Music" not finding songs:**
- The search uses the text as-is, so "Artist - Song" format works best
- Some songs may not be on Apple Music

**"Add to Playlist" failing:**
- Make sure the playlist exists first
- Or set it to "Ask Each Time" to choose dynamically

**Rate limiting:**
- Apple Music may throttle if you add too many songs too fast
- The Repeat action naturally paces requests
