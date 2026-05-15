import pandas as pd
import os
from datetime import datetime

class ExcelAgent:
    """
    Agent 1: Excel file को पढ़ता है, validate करता है, 
    और पिछली report के साथ compare करता है
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.previous_state = None
        
    def load_excel(self) -> pd.DataFrame:
        """Excel फाइल लोड करो"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")
        
        self.df = pd.read_excel(self.file_path, engine='openpyxl')
        print(f"✅ Loaded {len(self.df)} rows from {self.file_path}")
        return self.df
    
    def get_summary(self) -> dict:
        """Excel का सारांश निकालो (LLM के लिए)"""
        if self.df is None:
            self.load_excel()
            
        return {
            "rows": len(self.df),
            "columns": list(self.df.columns),
            "numeric_cols": list(self.df.select_dtypes(include=['number']).columns),
            "date_cols": list(self.df.select_dtypes(include=['datetime64']).columns),
            "null_counts": self.df.isnull().sum().to_dict(),
            "sample_data": self.df.head(5).to_dict(orient='records')
        }
    
    def get_changes(self) -> dict:
        """पिछली report से क्या बदला? (Learning के लिए जरूरी)"""
        # पिछली report load करो
        prev_file = f"data/reports/report_{datetime.now().strftime('%Y%m%d')}_prev.xlsx"
        if os.path.exists(prev_file):
            prev_df = pd.read_excel(prev_file)
            changes = {
                "row_count_change": len(self.df) - len(prev_df),
                "new_data": self.df[~self.df.index.isin(prev_df.index)] if len(self.df) > len(prev_df) else None
            }
            return changes
        return {"row_count_change": 0, "new_data": None}
    
    def archive_current(self):
        """Current report को archive करो (ताकि कल compare कर सके)"""
        archive_path = f"data/reports/report_{datetime.now().strftime('%Y%m%d')}.xlsx"
        os.makedirs("data/reports", exist_ok=True)
        self.df.to_excel(archive_path, index=False)
        print(f"📦 Archived to {archive_path}")
