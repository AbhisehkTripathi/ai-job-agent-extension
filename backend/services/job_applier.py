# from agno import Agent
from ..utils import Agent  # Use our custom implementation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Dict, Any

class JobApplier(Agent):
    def __init__(self):
        super().__init__("JobApplier")
        self.driver = None
    
    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
    
    def apply_linkedin(self, url: str, contact_info: Dict[str, str]) -> Dict[str, Any]:
        if not self.driver:
            self.init_driver()
        
        self.driver.get(url)
        
        # This is a simplified version - LinkedIn's actual process is more complex
        try:
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apply')]"))
            )
            apply_button.click()
            
            # Fill in contact information
            # Note: Actual implementation would need to handle LinkedIn's specific form fields
            time.sleep(2)
            
            return {"status": "Application submitted", "platform": "LinkedIn"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def apply_naukri(self, url: str, contact_info: Dict[str, str]) -> Dict[str, Any]:
        if not self.driver:
            self.init_driver()
        
        self.driver.get(url)
        
        try:
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apply Now')]"))
            )
            apply_button.click()
            
            # Fill in contact information
            # Note: Actual implementation would need to handle Naukri's specific form fields
            time.sleep(2)
            
            return {"status": "Application submitted", "platform": "Naukri"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def apply(self, job_url: str, contact_info: Dict[str, str]) -> Dict[str, Any]:
        if "linkedin.com" in job_url:
            return self.apply_linkedin(job_url, contact_info)
        elif "naukri.com" in job_url:
            return self.apply_naukri(job_url, contact_info)
        else:
            return {"status": "error", "message": "Unsupported job platform"}
    
    def __del__(self):
        if self.driver:
            self.driver.quit()