#!/usr/bin/env python3
"""
Keep-awake service for Replit Discord bot
Sends periodic pings to prevent the bot from going to sleep
"""

import requests
import time
import logging
import threading
from datetime import datetime, timedelta

class KeepAwakeService:
    def __init__(self, ping_interval_minutes=12):
        """
        Initialize the keep-awake service
        
        Args:
            ping_interval_minutes: How often to ping (default: 12 minutes)
        """
        self.ping_interval = ping_interval_minutes * 60  # Convert to seconds
        self.base_url = "http://localhost:5000"
        self.is_running = False
        self.thread = None
        
    def ping_self(self):
        """Send a ping to our own Flask server"""
        try:
            response = requests.get(f"{self.base_url}/ping", timeout=10)
            if response.status_code == 200:
                data = response.json()
                logging.info(f"🏓 Keep-awake ping successful: {data}")
                return True
            else:
                logging.warning(f"⚠️ Keep-awake ping failed with status: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"❌ Keep-awake ping error: {e}")
            return False
    
    def health_check(self):
        """Check if the Flask server is responding"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_keep_awake(self):
        """Main keep-awake loop"""
        logging.info(f"🚀 Keep-awake service started (ping every {self.ping_interval//60} minutes)")
        
        while self.is_running:
            try:
                # Wait for the interval
                time.sleep(self.ping_interval)
                
                if not self.is_running:
                    break
                
                # Send ping
                success = self.ping_self()
                
                if success:
                    next_ping = datetime.now() + timedelta(seconds=self.ping_interval)
                    logging.info(f"⏰ Next keep-awake ping scheduled for: {next_ping.strftime('%H:%M:%S')}")
                else:
                    logging.warning("⚠️ Keep-awake ping failed, will retry at next interval")
                    
            except Exception as e:
                logging.error(f"❌ Keep-awake service error: {e}")
                if self.is_running:
                    # Wait a bit before retrying on error
                    time.sleep(60)
    
    def start(self):
        """Start the keep-awake service in a background thread"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run_keep_awake, daemon=True)
            self.thread.start()
            logging.info("✅ Keep-awake service thread started")
    
    def stop(self):
        """Stop the keep-awake service"""
        if self.is_running:
            self.is_running = False
            if self.thread:
                self.thread.join(timeout=5)
            logging.info("🛑 Keep-awake service stopped")

# Global instance
keep_awake_service = KeepAwakeService(ping_interval_minutes=12)

def start_keep_awake():
    """Start the keep-awake service"""
    # Wait a bit for the Flask server to be ready
    time.sleep(10)
    keep_awake_service.start()

if __name__ == "__main__":
    # Test the service
    logging.basicConfig(level=logging.INFO)
    start_keep_awake()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        keep_awake_service.stop()