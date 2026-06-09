from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper.zillow_api import run_scraper
from reports.excel_report import generate_report
from datetime import datetime

scheduler = BlockingScheduler()

def scheduled_job():
    print(f"\n⏰ Auto run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_scraper()
    generate_report()
    print("✅ Job completed!")

 # Every day at 08:00
scheduler.add_job(
    scheduled_job,
    trigger=CronTrigger(hour=8, minute=0),
    id="daily_scraper",
    name="Daily Zillow Scraper",
    replace_existing=True
)

if __name__ == "__main__":
    print("🕐 Scheduler started...")
    print("📅 Scraping every day at 08:00")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped")
        scheduler.shutdown()