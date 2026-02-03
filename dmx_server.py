#!/usr/bin/env python3
"""
U`King DMX Server
Bridges the web controller to your USB-DMX hardware interface

Requirements:
    pip install flask flask-cors pyserial

Hardware Setup:
    1. Connect USB-DMX adapter (ENTTEC, DMXKing, etc.)
    2. Connect DMX cable from adapter to U`King fixture
    3. Set U`King to DMX mode (6 or 11 channel)
    4. Set starting DMX address to 1 (or whatever you prefer)

Usage:
    python dmx_server.py
    
Then open the HTML controller in your browser at:
    http://localhost:8080
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import serial.tools.list_ports
import struct
import time
import threading

app = Flask(__name__)
CORS(app)

class DMXController:
    def __init__(self, port=None, baudrate=250000):
        """
        Initialize DMX controller
        
        Args:
            port: Serial port for DMX interface (auto-detect if None)
            baudrate: 250000 for DMX512 (standard)
        """
        self.dmx_data = [0] * 512  # DMX universe (512 channels)
        self.serial_port = None
        self.running = False
        self.update_thread = None
        
        # Try to connect to DMX interface
        if port:
            self.connect(port, baudrate)
        else:
            self.auto_connect(baudrate)
    
    def auto_connect(self, baudrate=250000):
        """Auto-detect and connect to USB-DMX interface"""
        print("🔍 Scanning for USB-DMX interfaces...")
        
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"  Found: {port.device} - {port.description}")
            
            # Common USB-DMX adapter identifiers
            if any(keyword in port.description.lower() for keyword in 
                   ['dmx', 'enttec', 'ftdi', 'dmxking', 'usb serial']):
                try:
                    print(f"✅ Attempting connection to {port.device}...")
                    self.connect(port.device, baudrate)
                    return True
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    continue
        
        print("⚠️  No DMX interface found. Running in simulation mode.")
        return False
    
    def connect(self, port, baudrate=250000):
        """Connect to specific serial port"""
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_TWO,
                timeout=1
            )
            print(f"✅ Connected to DMX interface: {port}")
            self.start_updates()
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def set_channel(self, channel, value):
        """Set a single DMX channel (1-512)"""
        if 1 <= channel <= 512:
            self.dmx_data[channel - 1] = max(0, min(255, value))
    
    def set_channels(self, start_channel, values):
        """Set multiple consecutive DMX channels"""
        for i, value in enumerate(values):
            self.set_channel(start_channel + i, value)
    
    def send_dmx_packet(self):
        """Send DMX packet to hardware (ENTTEC protocol)"""
        if not self.serial_port:
            return False
        
        try:
            # ENTTEC USB-DMX Pro protocol
            # Header: 0x7E (start), 0x06 (label), length LSB, length MSB
            packet = bytearray()
            packet.append(0x7E)  # Start byte
            packet.append(0x06)  # Send DMX packet label
            
            # DMX data with start code
            dmx_packet = bytearray([0x00] + self.dmx_data)  # 0x00 = start code
            
            # Length (LSB, MSB)
            length = len(dmx_packet)
            packet.append(length & 0xFF)
            packet.append((length >> 8) & 0xFF)
            
            # Data
            packet.extend(dmx_packet)
            
            # End byte
            packet.append(0xE7)
            
            self.serial_port.write(packet)
            return True
            
        except Exception as e:
            print(f"❌ DMX send error: {e}")
            return False
    
    def start_updates(self):
        """Start background thread to continuously send DMX updates"""
        if self.running:
            return
        
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        print("🔄 DMX update loop started (44 Hz)")
    
    def _update_loop(self):
        """Background loop to send DMX at ~44Hz (standard refresh rate)"""
        while self.running:
            self.send_dmx_packet()
            time.sleep(1.0 / 44.0)  # ~44 Hz refresh
    
    def stop(self):
        """Stop DMX updates and close connection"""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)
        if self.serial_port:
            self.serial_port.close()
        print("🛑 DMX controller stopped")

# Global DMX controller instance
dmx = DMXController()

@app.route('/')
def index():
    """Serve the HTML controller"""
    try:
        with open('uking-dmx-controller.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>DMX Server Running</h1>
        <p>Place 'uking-dmx-controller.html' in the same directory as this script.</p>
        <p>Server is listening on http://localhost:8080</p>
        """

@app.route('/dmx', methods=['POST'])
def update_dmx():
    """Receive DMX updates from web controller"""
    data = request.json
    
    start_address = data.get('startAddress', 1)
    channels = data.get('channels', [])
    
    # Update DMX channels
    dmx.set_channels(start_address, channels)
    
    # Log for debugging
    print(f"📡 DMX Update - Addr: {start_address}, Channels: {channels}")
    
    return jsonify({
        'status': 'ok',
        'address': start_address,
        'channels_updated': len(channels)
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Get current DMX status"""
    return jsonify({
        'connected': dmx.serial_port is not None,
        'port': dmx.serial_port.port if dmx.serial_port else None,
        'running': dmx.running
    })

@app.route('/blackout', methods=['POST'])
def blackout():
    """Emergency blackout - set all channels to 0"""
    dmx.dmx_data = [0] * 512
    print("⬛ BLACKOUT ACTIVATED")
    return jsonify({'status': 'blackout'})

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           U`KING DMX SERVER - v1.0                           ║
    ║                                                              ║
    ║  Server running on: http://localhost:8080                    ║
    ║  Open in your browser to access the controller              ║
    ║                                                              ║
    ║  Keyboard Shortcuts (in browser):                           ║
    ║    SPACE - Blackout                                         ║
    ║    1-6   - Scene presets                                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Run Flask server
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        dmx.stop()
