#!/usr/bin/env python3
"""
WildGuard AI - Production Scheduler
Runs scans on schedule to achieve daily targets
"""

import asyncio
import schedule
import time
import logging
from datetime import datetime
from production_scanner import run_scheduled_scan
import os
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wildguard_scheduler.log'),
        logging.StreamHandler()
    ]
)

class WildGuardScheduler:
    """Production scheduler for continuous operation"""
    
    def __init__(self):
        self.is_running = False
        self.scan_count = 0
        self.total_results_today = 0
        self.start_time = datetime.now()
        
    def run_scan_job(self):
        """Job wrapper for scheduled scans"""
        if self.is_running:
            logging.warning("Previous scan still running, skipping...")
            return
        
        self.is_running = True
        
        try:
            # Run the async scan
            result = asyncio.run(run_scheduled_scan())
            
            self.scan_count += 1
            self.total_results_today += result['total_results']
            
            # Calculate daily projection
            hours_running = (datetime.now() - self.start_time).total_seconds() / 3600
            if hours_running > 0:
                projected_daily = int((self.total_results_today / hours_running) * 24)
            else:
                projected_daily = result['total_results'] * 24
            
            logging.info(f"📊 Daily Progress: {self.scan_count} scans, {self.total_results_today:,} results, projected: {projected_daily:,}")
            
        except Exception as e:
            logging.error(f"Scan job failed: {e}")
        
        finally:
            self.is_running = False

    def start_scheduler(self):
        """Start the production scheduler"""
        logging.info("🚀 Starting WildGuard Production Scheduler")
        logging.info("   Target: 200,000+ daily listings")
        logging.info("   Schedule: Every hour (24 scans/day)")
        
        # Schedule scans every hour
        schedule.every().hour.do(self.run_scan_job)
        
        # Optional: Run immediately on startup
        logging.info("🔥 Running initial scan...")
        self.run_scan_job()
        
        # Keep running
        logging.info("⏰ Scheduler active - scans every hour")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logging.info("🛑 Scheduler stopped by user")
        except Exception as e:
            logging.error(f"💥 Scheduler error: {e}")
            raise

    def start_high_frequency_scheduler(self):
        """High frequency scheduler for maximum throughput"""
        logging.info("🚀 Starting HIGH FREQUENCY WildGuard Scheduler")
        logging.info("   Target: 300,000+ daily listings")
        logging.info("   Schedule: Every 40 minutes (36 scans/day)")
        
        # Schedule scans every 40 minutes for higher throughput
        schedule.every(40).minutes.do(self.run_scan_job)
        
        # Run immediately
        logging.info("🔥 Running initial scan...")
        self.run_scan_job()
        
        # Keep running
        logging.info("⚡ High-frequency scheduler active - scans every 40 minutes")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            logging.info("🛑 High-frequency scheduler stopped")
        except Exception as e:
            logging.error(f"💥 Scheduler error: {e}")
            raise


def main():
    """Main entry point"""
    scheduler = WildGuardScheduler()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--high-frequency':
        scheduler.start_high_frequency_scheduler()
    else:
        scheduler.start_scheduler()


if __name__ == "__main__":
    main()
