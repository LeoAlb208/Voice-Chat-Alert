#!/usr/bin/env python3
"""
External uptime monitor for the Discord bot
This script can be run independently to ping the bot and keep it alive
"""

import requests
import time
import logging
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - UPTIME - %(levelname)s - %(message)s'
)

class UptimeMonitor:
    def __init__(self, target_url="http://localhost:5000", ping_interval_minutes=10):
        self.target_url = target_url
        self.ping_interval = ping_interval_minutes * 60
        self.running = True
        
    def ping_service(self):
        """Ping the service to keep it alive"""
        try:
            response = requests.get(f"{self.target_url}/ping", timeout=10)
            if response.status_code == 200:
                data = response.json()
                logging.info(f"✅ Ping successful: {data}")
                return True
            else:
                logging.error(f"❌ Ping failed with status: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"❌ Ping error: {e}")
            return False
    
    def health_check(self):
        """Check service health"""
        try:
            response = requests.get(f"{self.target_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                logging.info(f"💚 Health check passed: {data}")
                return True
            else:
                logging.warning(f"⚠️ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            logging.warning(f"⚠️ Health check error: {e}")
            return False
    
    def run(self):
        """Main monitoring loop"""
        logging.info(f"🚀 Uptime monitor started - pinging every {self.ping_interval//60} minutes")
        
        # Initial health check
        if not self.health_check():
            logging.warning("⚠️ Initial health check failed, but continuing...")
        
        while self.running:
            try:
                # Wait for interval
                time.sleep(self.ping_interval)
                
                if not self.running:
                    break
                
                # Ping the service
                success = self.ping_service()
                
                if success:
                    next_ping = datetime.now().replace(microsecond=0)
                    next_ping = next_ping.replace(second=next_ping.second + self.ping_interval)
                    logging.info(f"⏰ Next ping scheduled for: {next_ping}")
                else:
                    logging.warning("⚠️ Ping failed, service might be down")
                    
            except KeyboardInterrupt:
                logging.info("🛑 Monitor stopped by user")
                break
            except Exception as e:
                logging.error(f"❌ Monitor error: {e}")
                # Wait a bit before retrying
                time.sleep(60)
    
    def stop(self):
        """Stop the monitor"""
        self.running = False

if __name__ == "__main__":
    monitor = UptimeMonitor(ping_interval_minutes=10)
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        monitor.stop()
        logging.info("🛑 Uptime monitor stopped")
        sys.exit(0)