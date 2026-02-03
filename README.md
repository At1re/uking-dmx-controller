# U`King DMX Controller Setup Guide

## What I Built
A fully-functional web-based DMX controller for your U`King 5-beam laser light with:
- ✅ Audio-reactive mode (responds to bass/music)
- ✅ 6 scene presets
- ✅ Manual control of all channels
- ✅ Real-time visualizer
- ✅ Keyboard shortcuts

## Hardware You Need
1. **USB-DMX Interface** (one of these):
   - ENTTEC DMX USB Pro (~$150) - industry standard
   - DMXKing ultraDMX Micro (~$60) - solid budget option
   - Generic FTDI-based adapter (~$20-40) - works but less reliable

2. **DMX Cables**
   - 3-pin or 5-pin XLR cable (your U`King probably uses 3-pin)
   - You said you already have these ✅

3. **Your U`King Fixture**
   - Set it to DMX mode (check the manual - usually a button combo)
   - Use 6-channel mode (or 11-channel if you want more control)
   - Set DMX address to **001** (or whatever you prefer)

## Software Installation

### Step 1: Install Python Requirements
```bash
pip install flask flask-cors pyserial
```

### Step 2: Setup Files
Put these 3 files in the same folder:
- `dmx_server.py` (the Python server)
- `uking-dmx-controller.html` (the web interface)
- `README.md` (this file)

### Step 3: Connect Hardware
1. Plug USB-DMX adapter into your computer
2. Connect DMX cable: **Adapter OUT → U`King IN**
3. Power on your U`King fixture
4. Set it to DMX mode and address 001

### Step 4: Run the Server
```bash
python dmx_server.py
```

You should see:
```
🔍 Scanning for USB-DMX interfaces...
  Found: /dev/cu.usbserial-EN123456 - USB Serial
✅ Attempting connection to /dev/cu.usbserial-EN123456...
✅ Connected to DMX interface: /dev/cu.usbserial-EN123456
🔄 DMX update loop started (44 Hz)
```

### Step 5: Open Controller
Open your browser to: **http://localhost:8080**

## Using the Controller

### Scene Presets (or press keys 1-6)
1. **Blackout** - All off (SPACEBAR shortcut)
2. **Full Power** - Maximum output
3. **Slow Rotate** - Gentle rotating effect
4. **Fast Strobe** - High energy strobe
5. **Rainbow Cycle** - Automatic color cycling
6. **Chaos Mode** - Random everything

### Manual Controls
- **Color Select** - Click color buttons or use slider
- **Pattern Mode** - Change beam patterns
- **Strobe Speed** - Adjust flash rate
- **Rotation** - Spin speed
- **Master Dimmer** - Overall brightness

### Audio Reactive Mode
1. Toggle "Audio Input" switch
2. Allow microphone access when prompted
3. Adjust "Bass Sensitivity" slider
4. Lights will respond to music/bass automatically!

## Channel Mapping (U`King 6-Channel Mode)

| Channel | Function | Range |
|---------|----------|-------|
| CH1 | Color | 0-255 (R→G→B→Y→C) |
| CH2 | Pattern | 0-255 (different beam patterns) |
| CH3 | Strobe | 0-255 (slow → fast) |
| CH4 | Rotation | 0-255 (speed + direction) |
| CH5 | Dimmer | 0-255 (0=off, 255=full) |
| CH6 | Mode | 0-255 (sound/auto/dmx) |

## Troubleshooting

### "No DMX interface found"
- Check USB cable connection
- On Mac: run `ls /dev/cu.*` to see available ports
- On Windows: check Device Manager for COM ports
- On Linux: run `ls /dev/ttyUSB*`
- You may need to install FTDI drivers

### "Lights not responding"
- Verify U`King is in DMX mode (check display)
- Check DMX address matches (default: 001)
- Verify DMX cable is OUT → IN (not backwards)
- Try different DMX address in the controller

### "Audio not working"
- Allow microphone permissions in browser
- Adjust bass sensitivity slider
- Check if audio visualizer is showing movement
- Try speaking/making noise to test

### "Server won't start"
- Make sure port 8080 is not in use
- Kill any existing Python processes
- Try changing port in dmx_server.py

## Advanced: Serato Integration

To sync with Serato like your friend did:

1. **Use MIDI Mapping**:
   - Map Serato cue points to keyboard numbers 1-6
   - These trigger scene presets automatically
   
2. **Audio Routing**:
   - Route Serato output → Virtual Audio Cable → Controller
   - Or use Soundflower (Mac) / VB-Cable (Windows)
   
3. **OSC Control** (advanced):
   - Modify server to accept OSC messages
   - Use TouchOSC or similar to trigger scenes

## Tips for Gigs

1. **Test everything before the gig** - seriously
2. **Blackout = SPACEBAR** - remember this for emergencies
3. **Audio mode works best with bass-heavy tracks**
4. **Scene 6 (Chaos) is a crowd pleaser**
5. **Keep laptop plugged in** - DMX processing drains battery
6. **Bring backup DMX cables** - they fail at the worst times

## Next Steps

Want to add more features?
- Multi-fixture control (control multiple lights)
- BPM sync (tap tempo to match music)
- Timeline/cue list builder
- MIDI controller integration
- Mobile app version

Let me know what you need!

## Specifications

- **DMX Protocol**: DMX512-A standard
- **Update Rate**: 44 Hz (standard DMX refresh)
- **Channels**: 512 universe
- **Audio**: Web Audio API (real-time FFT analysis)
- **Browser**: Chrome/Edge recommended (best audio support)

---

Built for your setup with the U`King 5-beam laser. 
Enjoy the show! 🎉🎵💡
