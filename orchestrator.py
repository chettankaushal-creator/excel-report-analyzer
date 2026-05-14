from src.agents.excel_agent import ExcelAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.email_agent import EmailAgent
import os
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

load_dotenv()

class ReportOrchestrator:
    """
    🧠 THE BRAIN - सब कुछ यहाँ से control होता है
    """
    
    def __init__(self):
        self.excel_path = os.getenv("EXCEL_FILE_PATH", "data/daily_report.xlsx")
        self.excel_agent = ExcelAgent(self.excel_path)
        self.analysis_agent = AnalysisAgent()
        self.email_agent = EmailAgent()
        
    def run_daily_report(self):
        """
        पूरा workflow एक कमांड में
        """
        print(f"\n{'='*50}")
        print(f"🤖 Starting Daily Report at {datetime.now()}")
        print(f"{'='*50}\n")
        
        try:
            # Step 1: Excel पढ़ो
            print("📂 STEP 1: Loading Excel...")
            df = self.excel_agent.load_excel()
            summary = self.excel_agent.get_summary()
            changes = self.excel_agent.get_changes()
            print(f"   ✅ Loaded {summary['rows']} rows, {len(summary['columns'])} columns")
            
            # Step 2: Analysis करो (WITH LEARNING)
            print("\n🧠 STEP 2: AI Analysis (learning from past)...")
            analysis = self.analysis_agent.analyze(summary, changes)
            print(f"   ✅ Analysis complete\n")
            print(analysis)
            
            # Step 3: Email भेजो
            print("\n📧 STEP 3: Sending email...")
            success = self.email_agent.send_report(analysis, summary)
            
            # Step 4: Archive current report (for tomorrow's comparison)
            self.excel_agent.archive_current()
            
            print(f"\n✅ ALL DONE! Email sent: {success}")
            return True
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            # TODO: Send error alert
            return False
    
    def schedule_daily(self, time_str: str = "08:00"):
        """
        Daily schedule set करो
        """
        schedule.every().day.at(time_str).do(self.run_daily_report)
        print(f"⏰ Scheduled daily report at {time_str}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
