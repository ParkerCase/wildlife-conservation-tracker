# international_platforms.py
# New international platform scrapers for wildlife conservation monitoring
# Phase 2: International Platform Research & Implementation

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import os
import base64
from fake_useragent import UserAgent
import random
import requests
import re


class AliExpressScanner:
    """AliExpress scraper for global marketplace monitoring"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.search_url = "https://www.aliexpress.us/w/wholesale"
        
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]  # Limit for demo
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.ua.random,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            for term in search_terms:
                url = f"{self.search_url}?SearchText={term}&SortType=default"
                
                try:
                    await page.goto(url, timeout=20000)
                    await page.wait_for_timeout(3000)
                    
                    # Wait for products to load
                    await page.wait_for_selector('.search-item-card-wrapper-gallery', timeout=10000)
                    
                    # Extract product data
                    products = await page.evaluate('''
                        () => {
                            const products = [];
                            const productElements = document.querySelectorAll('.search-item-card-wrapper-gallery');
                            
                            productElements.forEach((el, index) => {
                                if (index >= 5) return; // Limit per term
                                
                                const titleEl = el.querySelector('h1, h3, a[title], .item-title');
                                const priceEl = el.querySelector('.price, .notranslate, [class*="price"]');
                                const imageEl = el.querySelector('img');
                                const linkEl = el.querySelector('a');
                                
                                const title = titleEl ? titleEl.textContent.trim() : '';
                                const price = priceEl ? priceEl.textContent.trim() : '';
                                const image = imageEl ? imageEl.src : '';
                                const link = linkEl ? linkEl.href : '';
                                
                                if (title && link) {
                                    products.push({
                                        title: title,
                                        price: price,
                                        image: image,
                                        url: link.startsWith('http') ? link : 'https://www.aliexpress.com' + link
                                    });
                                }
                            });
                            
                            return products;
                        }
                    ''')
                    
                    for product in products:
                        product['search_term'] = term
                        product['platform'] = 'aliexpress'
                        results.append(product)
                        
                    logging.info(f"AliExpress: Found {len(products)} products for '{term}'")
                    
                    # Rate limiting
                    await asyncio.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logging.error(f"AliExpress scan error for {term}: {e}")
                    
            await browser.close()
            
        return results


class GumtreeScanner:
    """Gumtree scraper for UK/Australia classifieds"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.regions = {
            'uk': 'https://www.gumtree.com/search',
            'au': 'https://www.gumtree.com.au/s-ad'
        }
        
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.ua.random,
                viewport={'width': 1366, 'height': 768}
            )
            page = await context.new_page()
            
            for region, base_url in self.regions.items():
                for term in search_terms:
                    if region == 'uk':
                        url = f"{base_url}?search_category=all&search_location=&q={term}"
                    else:  # Australia
                        url = f"{base_url}/{term}/k0"
                        
                    try:
                        await page.goto(url, timeout=20000)
                        await page.wait_for_timeout(2000)
                        
                        # UK Gumtree selectors
                        if region == 'uk':
                            listings = await page.query_selector_all('article.listing-maxi')
                            
                            for listing in listings[:3]:  # Limit per region/term
                                title_el = await listing.query_selector('h2 a, .listing-title a')
                                price_el = await listing.query_selector('.listing-price strong')
                                location_el = await listing.query_selector('.listing-location span')
                                link_el = await listing.query_selector('h2 a, .listing-title a')
                                
                                title = await title_el.inner_text() if title_el else ''
                                price = await price_el.inner_text() if price_el else ''
                                location = await location_el.inner_text() if location_el else ''
                                link = await link_el.get_attribute('href') if link_el else ''
                                
                                if title and link:
                                    if not link.startswith('http'):
                                        link = f'https://www.gumtree.com{link}'
                                        
                                    results.append({
                                        'title': title.strip(),
                                        'price': price.strip(),
                                        'location': location.strip(),
                                        'url': link,
                                        'search_term': term,
                                        'platform': 'gumtree',
                                        'region': region
                                    })
                        
                        # Australia Gumtree has different structure
                        else:
                            listings = await page.query_selector_all('.user-ad-row, article')
                            
                            for listing in listings[:3]:
                                title_el = await listing.query_selector('a.user-ad-row-new-design__title-link, h3 a')
                                price_el = await listing.query_selector('.user-ad-price__amount, .ad-price')
                                location_el = await listing.query_selector('.user-ad-row-new-design__location, .ad-location')
                                link_el = await listing.query_selector('a.user-ad-row-new-design__title-link, h3 a')
                                
                                title = await title_el.inner_text() if title_el else ''
                                price = await price_el.inner_text() if price_el else ''
                                location = await location_el.inner_text() if location_el else ''
                                link = await link_el.get_attribute('href') if link_el else ''
                                
                                if title and link:
                                    if not link.startswith('http'):
                                        link = f'https://www.gumtree.com.au{link}'
                                        
                                    results.append({
                                        'title': title.strip(),
                                        'price': price.strip(),
                                        'location': location.strip(),
                                        'url': link,
                                        'search_term': term,
                                        'platform': 'gumtree',
                                        'region': region
                                    })
                        
                        logging.info(f"Gumtree {region.upper()}: Found {len(listings[:3])} listings for '{term}'")
                        
                        # Rate limiting
                        await asyncio.sleep(random.uniform(2, 5))
                        
                    except Exception as e:
                        logging.error(f"Gumtree {region} scan error for {term}: {e}")
                        
            await browser.close()
            
        return results


class OLXScanner:
    """OLX scraper for global developing markets"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.country_domains = {
            'pl': 'https://www.olx.pl/oferty',  # Poland
            'in': 'https://www.olx.in/all-results',  # India
            'br': 'https://www.olx.com.br/brasil',  # Brazil
            'pk': 'https://www.olx.com.pk/all-results',  # Pakistan
        }
        
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:2]  # Limit for demo
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.ua.random,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            for country, base_url in self.country_domains.items():
                for term in search_terms:
                    url = f"{base_url}?q={term}"
                    
                    try:
                        await page.goto(url, timeout=20000)
                        await page.wait_for_timeout(3000)
                        
                        # Common OLX selectors (may vary by country)
                        listings = await page.query_selector_all('[data-cy="l-card"], .offer-wrapper, article')
                        
                        for listing in listings[:3]:  # Limit per country/term
                            title_el = await listing.query_selector('h3, h4, .title, [data-cy="ad-card-title"]')
                            price_el = await listing.query_selector('.price, [data-testid="ad-price"], .offer-price')
                            location_el = await listing.query_selector('.location, .city-name, [data-testid="location-date"]')
                            link_el = await listing.query_selector('a')
                            image_el = await listing.query_selector('img')
                            
                            title = await title_el.inner_text() if title_el else ''
                            price = await price_el.inner_text() if price_el else ''
                            location = await location_el.inner_text() if location_el else ''
                            link = await link_el.get_attribute('href') if link_el else ''
                            image = await image_el.get_attribute('src') if image_el else ''
                            
                            if title and link:
                                if not link.startswith('http'):
                                    domain_base = base_url.split('/')[0] + '//' + base_url.split('/')[2]
                                    link = f'{domain_base}{link}'
                                    
                                results.append({
                                    'title': title.strip(),
                                    'price': price.strip(),
                                    'location': location.strip(),
                                    'url': link,
                                    'image': image,
                                    'search_term': term,
                                    'platform': 'olx',
                                    'country': country
                                })
                        
                        logging.info(f"OLX {country.upper()}: Found {len(listings[:3])} listings for '{term}'")
                        
                        # Rate limiting
                        await asyncio.sleep(random.uniform(3, 6))
                        
                    except Exception as e:
                        logging.error(f"OLX {country} scan error for {term}: {e}")
                        
            await browser.close()
            
        return results


class MercadoLibreScanner:
    """MercadoLibre scraper for Latin America"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.country_domains = {
            'mx': 'https://listado.mercadolibre.com.mx',  # Mexico
            'ar': 'https://listado.mercadolibre.com.ar',  # Argentina
            'br': 'https://lista.mercadolivre.com.br',    # Brazil
            'co': 'https://listado.mercadolibre.com.co',  # Colombia
            'cl': 'https://listado.mercadolibre.cl',      # Chile
        }
        
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:2]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.ua.random,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            for country, base_url in self.country_domains.items():
                for term in search_terms:
                    url = f"{base_url}/{term}"
                    
                    try:
                        await page.goto(url, timeout=20000)
                        await page.wait_for_timeout(3000)
                        
                        # Wait for results to load
                        await page.wait_for_selector('.ui-search-results', timeout=10000)
                        
                        # Extract products
                        products = await page.evaluate('''
                            () => {
                                const products = [];
                                const productElements = document.querySelectorAll('.ui-search-result, .item__info');
                                
                                productElements.forEach((el, index) => {
                                    if (index >= 4) return; // Limit per country/term
                                    
                                    const titleEl = el.querySelector('.ui-search-item__title, h2 a, .item__title');
                                    const priceEl = el.querySelector('.price-tag, .ui-search-price__second-line, .item__price');
                                    const linkEl = el.querySelector('a, .ui-search-link');
                                    const imageEl = el.querySelector('img');
                                    const locationEl = el.querySelector('.ui-search-item__location, .item__location');
                                    
                                    const title = titleEl ? titleEl.textContent.trim() : '';
                                    const price = priceEl ? priceEl.textContent.trim() : '';
                                    const link = linkEl ? linkEl.href : '';
                                    const image = imageEl ? imageEl.src : '';
                                    const location = locationEl ? locationEl.textContent.trim() : '';
                                    
                                    if (title && link) {
                                        products.push({
                                            title: title,
                                            price: price,
                                            location: location,
                                            url: link,
                                            image: image
                                        });
                                    }
                                });
                                
                                return products;
                            }
                        ''')
                        
                        for product in products:
                            product['search_term'] = term
                            product['platform'] = 'mercadolibre'
                            product['country'] = country
                            results.append(product)
                            
                        logging.info(f"MercadoLibre {country.upper()}: Found {len(products)} products for '{term}'")
                        
                        # Rate limiting
                        await asyncio.sleep(random.uniform(3, 5))
                        
                    except Exception as e:
                        logging.error(f"MercadoLibre {country} scan error for {term}: {e}")
                        
            await browser.close()
            
        return results


class TaobaoScanner:
    """Taobao scraper for China marketplace (with special handling)"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.search_url = "https://s.taobao.com/search"
        
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:2]  # Very limited for demo
        
        # Note: Taobao has sophisticated anti-bot measures
        # In production, consider using specialized proxy services
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.ua.random,
                viewport={'width': 1920, 'height': 1080},
                extra_http_headers={
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            )
            page = await context.new_page()
            
            for term in search_terms:
                url = f"{self.search_url}?q={term}&sort=default"
                
                try:
                    await page.goto(url, timeout=30000)
                    await page.wait_for_timeout(5000)  # Longer wait for anti-bot checks
                    
                    # Check if we hit anti-bot measures
                    if await page.query_selector('.nc_wrapper, .J_MIDDLEWARE_ERROR'):
                        logging.warning(f"Taobao anti-bot detected for {term}, skipping")
                        continue
                    
                    # Extract data from page source (Taobao loads data via JavaScript)
                    page_content = await page.content()
                    
                    # Try to extract from window.g_page_config or similar data structures
                    products_data = await page.evaluate('''
                        () => {
                            try {
                                // Look for product data in various possible locations
                                let data = [];
                                
                                // Check window.g_page_config
                                if (window.g_page_config && window.g_page_config.mods) {
                                    const itemlist = window.g_page_config.mods.itemlist;
                                    if (itemlist && itemlist.data && itemlist.data.auctions) {
                                        data = itemlist.data.auctions.slice(0, 3); // Limit results
                                    }
                                }
                                
                                // Fallback: try to parse from DOM
                                if (data.length === 0) {
                                    const items = document.querySelectorAll('.item, .J_MouserOnverReq');
                                    items.forEach((item, index) => {
                                        if (index >= 3) return;
                                        
                                        const titleEl = item.querySelector('.title a, .pic-box-inner .title');
                                        const priceEl = item.querySelector('.price .g_price, .view_price');
                                        const linkEl = item.querySelector('.title a, .pic-box-inner a');
                                        
                                        if (titleEl && linkEl) {
                                            data.push({
                                                title: titleEl.textContent.trim(),
                                                view_price: priceEl ? priceEl.textContent.trim() : '',
                                                detail_url: linkEl.href
                                            });
                                        }
                                    });
                                }
                                
                                return data;
                            } catch (e) {
                                console.error('Taobao data extraction error:', e);
                                return [];
                            }
                        }
                    ''')
                    
                    for product in products_data:
                        # Handle both API data and DOM scraped data
                        title = product.get('title', '') or product.get('raw_title', '')
                        price = product.get('view_price', '') or product.get('view_price', '')
                        url = product.get('detail_url', '') or product.get('nid', '')
                        
                        if url and not url.startswith('http'):
                            url = f'https://item.taobao.com/item.htm?id={url}'
                            
                        if title and url:
                            results.append({
                                'title': title,
                                'price': price,
                                'url': url,
                                'search_term': term,
                                'platform': 'taobao',
                                'country': 'cn'
                            })
                    
                    logging.info(f"Taobao: Found {len(products_data)} products for '{term}'")
                    
                    # Longer rate limiting for Taobao
                    await asyncio.sleep(random.uniform(5, 10))
                    
                except Exception as e:
                    logging.error(f"Taobao scan error for {term}: {e}")
                    
            await browser.close()
            
        return results
