from abc import ABC, abstractmethod 
import time
import random
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

from src.utils.config_loader import config_loader, load_countries
from src.extract.cached import PathBuilder, Serializer, Agechecker
from src.utils.logger import get_logger

logger = get_logger('extraction')


class BaseExtractor(ABC):
    """Abstract base class for all extractors."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.path_builder = PathBuilder()
        self.serializer = Serializer()
        self.age_checker = Agechecker(self.path_builder)
        self.logger.info(f"{self.__class__.__name__} initialized")
    
    def get_active_countries(self) -> List[Dict]:
        countries = load_countries()
        return [c for c in countries if c.get('is_active', True)]
    
    def check_cache(self, country_code: str) -> Optional[Dict]:
        """Check if fresh cache exists."""
        latest = self.age_checker.latest_raw(country_code)
        
        if latest and self.age_checker.is_flesh(latest):
            self.logger.info(f"Cache HIT for {country_code}")
            return self.serializer.load(latest)
        
        self.logger.info(f"Cache MISS for {country_code}")
        return None
    
    def save_data_cache(self, country_code: str, data: Dict) -> None:
        """Save data to cache."""
        source_type = self.get_source_type()
        filepath = self.path_builder.get_raw_path(country_code, source_type)
        self.serializer.save(data, filepath)
        self.logger.info(f"Saved to cache: {filepath}")
    
    
    def extract_country(self, country_code: str) -> Optional[Dict]:
        """Orchestrator: check cache → extract → save."""
        cached_data = self.check_cache(country_code)
        if cached_data:
            return cached_data
        
        self.logger.info(f"Cache MISS for {country_code}, extracting fresh")
        data = self._extract_from_source(country_code)  
        
        if data:
            self.save_data_cache(country_code, data)
        
        return data
    
    def run(self) -> List[Dict]:
        """Extract data for all active countries."""
        active_countries = self.get_active_countries()
        results = []
        
        self.logger.info(f"Processing {len(active_countries)} countries")
        
        for country in active_countries:
            code = country['code']
            name = country['name']
            
            self.logger.info(f"Processing {name} ({code})")
            
            data = self.extract_country(code)
            
            if data:
                results.append({
                    "country_code": code,
                    "country_name": name,
                    "data": data,
                    "data_source": self.get_source_type()
                })
            
            delay = self.config['extraction'].get('request_delay_seconds', 2)
            self.logger.info(f" Waiting {delay} seconds...")
            time.sleep(delay)
        
        self.logger.info(f"✅ Extraction complete: {len(results)} countries")
        return results
    
    # ========== ABSTRACT METHODS ==========
    
    @abstractmethod
    def get_source_type(self) -> str:
        """Return source type."""
        pass
    
    @abstractmethod
    def _extract_from_source(self, country_code: str) -> Optional[Dict]:
        """Actual extraction logic. Child must implement."""
        pass


# ============================================
# TIKTOK EXTRACTOR
# ============================================

class Tiktok(BaseExtractor):
    """TikTok-specific extractor."""
    
    def get_source_type(self) -> str:
        return "tiktok"
    
    def _extract_from_source(self, country_code: str) -> Optional[Dict]:
        """Extract data from TikTok using Playwright + Stealth."""
        max_retries=self.config['extraction'].get('max_retries', 3)
        base_delay=self.config['extraction'].get('request_delay_seconds', 2)
        for Attempt in range(1, max_retries +1):
            try:
                self.logger.info(f"Attemps {Attempt}/{max_retries} for {country_code}")
                url = f"https://www.tiktok.com/trending?country={country_code}"
                self.logger.info(f"Extracting from: {url}")
                
                
                with Stealth().use_sync(sync_playwright()) as p:
                        browser = p.chromium.launch(
                            headless=False,
                            slow_mo=800,
                            args=[
                                "--no-sandbox",
                                "--disable-blink-features=AutomationControlled",
                                "--disable-dev-shm-usage",
                                "--disable-infobars",
                                "--start-maximized",
                                "--disable-features=IsolatedOrigins,site-per-process"
                            ]
                        )
                        
                        context = browser.new_context(
                            viewport={"width": 1366, "height": 768},
                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            locale="en-US",
                            timezone_id="Africa/Nairobi"
                        )
                        
                        context.add_init_script("""
                            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                            Object.defineProperty(navigator, 'language', {get: () => ['en-US', 'en']});
                        """)
                        
                        page = context.new_page()
                        
                        # Stealth is ALREADY applied by Stealth().use_sync()
                        
                        self.logger.info(f"Navigating to {url}")
                        page.goto(url, wait_until="networkidle", timeout=60000)
                        
                        time.sleep(random.uniform(2, 5))
                        
                        for _ in range(3):
                            page.evaluate("window.scrollBy(0, 1200)")
                            time.sleep(random.uniform(1, 3))
                        
                        html_content = page.content()
                        data = self._extract_hidden_json(html_content)
                        
                        browser.close()
                        
                        if data:
                            self.logger.info(f"Well Extracted data for {country_code}")
                            return data
                        else:
                            self.logger.warning(f"Ohhh No data for {country_code}")
                                
                            
            except Exception as e:
                    self.logger.error(f"Error extracting {country_code}: {e}")
                    if Attempt < max_retries:
                        wait_time=base_delay * (2 ** (Attempt -1))
                        self.logger.info(f"Waiting time {wait_time} seconds before we rty")
                        time.sleep(wait_time)
                    else:
                        self.logger.info(f"all {Attempt} attempts has failed for {country_code}")    
                            
        return None
        

    def _extract_hidden_json(self, html_content: str) -> Optional[Dict]:
        """Extract TikTok's hidden JSON."""
        patterns = [
        r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
        r'<script id="__STATE__"[^>]*>(.*?)</script>',
        r'<script[^>]*video[^>]*>(.*?)</script>',
        r'<script[^>]*itemStruct[^>]*>(.*?)</script>']
        
    
    
        for pattern in patterns:
            match = re.search(pattern, html_content, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                    # Check if it has video data
                    if 'itemStruct' in str(data) or 'video' in str(data):
                        self.logger.info(f"Found video data using pattern: {pattern[:50]}...")
                        return data
                except:
                    continue
    
        self.logger.warning("Could not find video data in any script")
        return None


# ============================================
# MAIN ENTRY POINT : Testing stuff
# ============================================

def main():
    """Run extraction and display summary."""
    print("\n" + "="*60)
    print("TIKTOK TRENDS EXTRACTION - EAST AFRICA")
    print("="*60)
    
    config = config_loader()
    extractor = Tiktok(config)
    results = extractor.run()
    
    print("\n" + "="*60)
    print("EXTRACTION SUMMARY")
    print("="*60)
    for r in results:
        print(f"{r['country_name']} ({r['country_code']})")
    print("="*60)


if __name__ == "__main__":
    main()