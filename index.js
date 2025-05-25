// 3-Platform Wildlife Trade Detector: Amazon + eBay + Craigslist
// File: index.js

const sqlite3 = require("sqlite3").verbose();
const express = require("express");
const puppeteer = require("puppeteer");
const crypto = require("crypto");
const Anthropic = require("@anthropic-ai/sdk");
require("dotenv").config();

// Initialize Anthropic client
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Platform configuration
const PLATFORM_CONFIG = {
  ebay: {
    clientId: process.env.EBAY_CLIENT_ID,
    clientSecret: process.env.EBAY_CLIENT_SECRET,
    baseUrl: "https://api.sandbox.ebay.com",
  },
  amazon: {
    accessKey: process.env.AMAZON_ACCESS_KEY,
    secretKey: process.env.AMAZON_SECRET_KEY,
    partnerTag: process.env.AMAZON_PARTNER_TAG,
    region: "us-east-1",
    host: "webservices.amazon.com",
    uri: "/paapi5/searchitems",
  },
};

// Initialize SQLite database
const db = new sqlite3.Database("./wildlife_detector.db");

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS listings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      platform TEXT,
      platform_id TEXT,
      title TEXT,
      description TEXT,
      price TEXT,
      images TEXT,
      listing_url TEXT,
      location TEXT,
      seller_info TEXT,
      scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      
      image_score REAL,
      text_score REAL,
      risk_score REAL,
      flags TEXT,
      analysis_result TEXT,
      status TEXT DEFAULT 'pending',
      
      UNIQUE(platform, platform_id)
    )
  `);
});

// Wildlife keywords optimized for US marketplaces
const WILDLIFE_KEYWORDS = [
  "ivory",
  "antique ivory",
  "vintage ivory",
  "elephant ivory",
  "rhino horn",
  "rhinoceros horn",
  "tiger tooth",
  "tiger claw",
  "tiger bone",
  "tiger skin",
  "pangolin scale",
  "pangolin armor",
  "turtle shell",
  "tortoise shell",
  "hawksbill",
  "shark fin",
  "shark tooth",
  "elephant hair",
  "elephant tail",
  "scrimshaw",
  "whale bone",
  "whalebone",
  "coral jewelry",
  "black coral",
  "leopard skin",
  "cheetah fur",
  "leopard fur",
  "bear gall",
  "bear bile",
  "bear paw",
  "seahorse dried",
  "sea turtle",
  "exotic leather",
  "python skin",
  "crocodile leather",
];

// 1. eBay API Search (Enhanced)
async function searchEbayAPI(searchTerm, maxResults = 20) {
  console.log(`🔍 eBay API: Searching for "${searchTerm}"`);

  try {
    const accessToken = await getEbayAccessToken();
    const searchUrl = `${PLATFORM_CONFIG.ebay.baseUrl}/buy/browse/v1/item_summary/search`;

    const params = new URLSearchParams({
      q: searchTerm,
      limit: Math.min(maxResults, 50),
      fieldgroups: "MATCHING_ITEMS,EXTENDED",
      filter: "buyingOptions:{FIXED_PRICE|AUCTION}", // Include both auction and buy-it-now
    });

    const response = await fetch(`${searchUrl}?${params}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=US,zip=94105",
      },
    });

    if (!response.ok) {
      throw new Error(
        `eBay API error: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();

    if (!data.itemSummaries || data.itemSummaries.length === 0) {
      console.log(`⚠️ eBay: No items found for "${searchTerm}"`);
      return [];
    }

    const listings = data.itemSummaries.map((item) => ({
      platform: "ebay",
      platform_id: item.itemId,
      title: item.title,
      description: item.shortDescription || "",
      price: item.price
        ? `${item.price.currency} ${item.price.value}`
        : "See listing",
      url: item.itemWebUrl,
      image: item.image ? item.image.imageUrl : null,
      location: item.itemLocation
        ? `${item.itemLocation.city || ""}, ${
            item.itemLocation.stateOrProvince || ""
          } ${item.itemLocation.country || ""}`.trim()
        : "Not specified",
      seller_info: JSON.stringify({
        username: item.seller?.username || "Unknown",
        feedbackPercentage: item.seller?.feedbackPercentage || 0,
        feedbackScore: item.seller?.feedbackScore || 0,
      }),
      searchTerm,
    }));

    console.log(
      `✅ eBay: Found ${listings.length} listings for "${searchTerm}"`
    );
    return listings;
  } catch (error) {
    console.error(`❌ eBay API error for "${searchTerm}": ${error.message}`);
    return [];
  }
}

async function getEbayAccessToken() {
  const credentials = Buffer.from(
    `${PLATFORM_CONFIG.ebay.clientId}:${PLATFORM_CONFIG.ebay.clientSecret}`
  ).toString("base64");

  const response = await fetch(
    `${PLATFORM_CONFIG.ebay.baseUrl}/identity/v1/oauth2/token`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: `Basic ${credentials}`,
      },
      body: "grant_type=client_credentials&scope=https://api.ebay.com/oauth/api_scope",
    }
  );

  if (!response.ok) {
    throw new Error(`eBay OAuth failed: ${response.status}`);
  }

  const data = await response.json();
  return data.access_token;
}

// 2. Amazon Product Advertising API
async function searchAmazonAPI(searchTerm, maxResults = 20) {
  console.log(`🔍 Amazon API: Searching for "${searchTerm}"`);

  try {
    if (
      !PLATFORM_CONFIG.amazon.accessKey ||
      !PLATFORM_CONFIG.amazon.secretKey
    ) {
      console.log("⚠️ Amazon API credentials not configured");
      return [];
    }

    const requestPayload = {
      Keywords: searchTerm,
      Resources: [
        "Images.Primary.Large",
        "ItemInfo.Title",
        "ItemInfo.Features",
        "Offers.Listings.Price",
        "Offers.Listings.DeliveryInfo.IsAmazonFulfilled",
      ],
      PartnerTag: PLATFORM_CONFIG.amazon.partnerTag,
      PartnerType: "Associates",
      Marketplace: "www.amazon.com",
      ItemCount: Math.min(maxResults, 10), // Amazon API limit
      SearchIndex: "All",
    };

    const headers = await getAmazonAPIHeaders(JSON.stringify(requestPayload));

    const response = await fetch(
      `https://${PLATFORM_CONFIG.amazon.host}${PLATFORM_CONFIG.amazon.uri}`,
      {
        method: "POST",
        headers,
        body: JSON.stringify(requestPayload),
      }
    );

    if (!response.ok) {
      throw new Error(
        `Amazon API error: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();

    if (!data.SearchResult || !data.SearchResult.Items) {
      console.log(`⚠️ Amazon: No items found for "${searchTerm}"`);
      return [];
    }

    const listings = data.SearchResult.Items.map((item) => ({
      platform: "amazon",
      platform_id: item.ASIN,
      title: item.ItemInfo.Title.DisplayValue,
      description: item.ItemInfo.Features
        ? item.ItemInfo.Features.DisplayValues.join(" ")
        : "",
      price:
        item.Offers && item.Offers.Listings[0]
          ? `${item.Offers.Listings[0].Price.Currency} ${item.Offers.Listings[0].Price.Amount}`
          : "Price not available",
      url: item.DetailPageURL,
      image:
        item.Images && item.Images.Primary
          ? item.Images.Primary.Large.URL
          : null,
      location: "Amazon",
      seller_info: JSON.stringify({
        amazonFulfilled:
          item.Offers && item.Offers.Listings[0]
            ? item.Offers.Listings[0].DeliveryInfo.IsAmazonFulfilled
            : false,
      }),
      searchTerm,
    }));

    console.log(
      `✅ Amazon: Found ${listings.length} listings for "${searchTerm}"`
    );
    return listings;
  } catch (error) {
    console.error(`❌ Amazon API error for "${searchTerm}": ${error.message}`);
    return [];
  }
}

// Amazon API Authentication (AWS Signature Version 4)
async function getAmazonAPIHeaders(payload) {
  const timestamp = new Date().toISOString().replace(/[:\-]|\.\d{3}/g, "");
  const date = timestamp.substr(0, 8);

  const algorithm = "AWS4-HMAC-SHA256";
  const credentialScope = `${date}/${PLATFORM_CONFIG.amazon.region}/ProductAdvertisingAPI/aws4_request`;
  const credential = `${PLATFORM_CONFIG.amazon.accessKey}/${credentialScope}`;

  // Create canonical request
  const canonicalHeaders = [
    `content-encoding:amz-1.0`,
    `content-type:application/json; charset=utf-8`,
    `host:${PLATFORM_CONFIG.amazon.host}`,
    `x-amz-date:${timestamp}`,
    `x-amz-target:com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems`,
  ].join("\n");

  const signedHeaders =
    "content-encoding;content-type;host;x-amz-date;x-amz-target";
  const payloadHash = crypto.createHash("sha256").update(payload).digest("hex");

  const canonicalRequest = [
    "POST",
    PLATFORM_CONFIG.amazon.uri,
    "",
    canonicalHeaders,
    "",
    signedHeaders,
    payloadHash,
  ].join("\n");

  // Create string to sign
  const canonicalRequestHash = crypto
    .createHash("sha256")
    .update(canonicalRequest)
    .digest("hex");
  const stringToSign = [
    algorithm,
    timestamp,
    credentialScope,
    canonicalRequestHash,
  ].join("\n");

  // Calculate signature
  const signingKey = getSignatureKey(
    PLATFORM_CONFIG.amazon.secretKey,
    date,
    PLATFORM_CONFIG.amazon.region,
    "ProductAdvertisingAPI"
  );
  const signature = crypto
    .createHmac("sha256", signingKey)
    .update(stringToSign)
    .digest("hex");

  const authorization = `${algorithm} Credential=${credential}, SignedHeaders=${signedHeaders}, Signature=${signature}`;

  return {
    "Content-Encoding": "amz-1.0",
    "Content-Type": "application/json; charset=utf-8",
    Host: PLATFORM_CONFIG.amazon.host,
    "X-Amz-Date": timestamp,
    "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems",
    Authorization: authorization,
  };
}

function getSignatureKey(key, dateStamp, regionName, serviceName) {
  const kDate = crypto
    .createHmac("sha256", "AWS4" + key)
    .update(dateStamp)
    .digest();
  const kRegion = crypto
    .createHmac("sha256", kDate)
    .update(regionName)
    .digest();
  const kService = crypto
    .createHmac("sha256", kRegion)
    .update(serviceName)
    .digest();
  const kSigning = crypto
    .createHmac("sha256", kService)
    .update("aws4_request")
    .digest();
  return kSigning;
}

// 3. Enhanced Craigslist Scraper
async function scrapeCraigslist(searchTerm, maxResults = 20) {
  console.log(`🔍 Craigslist: Scraping for "${searchTerm}"`);

  const browser = await puppeteer.launch({
    headless: "new",
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-features=VizDisplayCompositor",
      "--disable-blink-features=AutomationControlled",
      '--proxy-server="direct://"',
      "--proxy-bypass-list=*",
    ],
  });

  try {
    const page = await browser.newPage();

    // Better stealth
    await page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    );
    await page.setViewport({ width: 1366, height: 768 });

    // Set extra headers
    await page.setExtraHTTPHeaders({
      "Accept-Language": "en-US,en;q=0.9",
      Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    });

    // Try different regions with delay
    const regions = ["sfbay", "newyork", "losangeles"];
    let allListings = [];

    for (const region of regions) {
      if (allListings.length >= maxResults) break;

      try {
        console.log(`  Trying ${region}...`);
        const searchUrl = `https://${region}.craigslist.org/search/sss?query=${encodeURIComponent(
          searchTerm
        )}`;

        await page.goto(searchUrl, {
          waitUntil: "domcontentloaded",
          timeout: 20000,
        });

        await page.waitForTimeout(3000); // Longer delay

        const listings = await page.evaluate(
          (maxResults, region, searchTerm) => {
            // ... (same extraction logic as before)
          },
          maxResults - allListings.length,
          region,
          searchTerm
        );

        allListings.push(...listings);
        console.log(`✅ ${region}: Found ${listings.length} listings`);

        // Longer delay between regions
        await page.waitForTimeout(5000);
      } catch (error) {
        console.log(`⚠️ ${region} failed: ${error.message}`);
        continue;
      }
    }

    return allListings;
  } catch (error) {
    console.error(`❌ Craigslist error: ${error.message}`);
    return [];
  } finally {
    await browser.close();
  }
}

async function scrapeEtsy(searchTerm, maxResults = 20) {
  console.log(`🔍 Etsy: Scraping for "${searchTerm}"`);

  const browser = await puppeteer.launch({ headless: "new" });

  try {
    const page = await browser.newPage();
    await page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    );

    const searchUrl = `https://www.etsy.com/search?q=${encodeURIComponent(
      searchTerm
    )}&explicit=1&category=vintage`;
    await page.goto(searchUrl, {
      waitUntil: "domcontentloaded",
      timeout: 15000,
    });

    await page.waitForTimeout(2000);

    const listings = await page.evaluate((maxResults) => {
      const items = document.querySelectorAll('[data-test-id="listing-card"]');
      const results = [];

      for (let i = 0; i < Math.min(items.length, maxResults); i++) {
        const item = items[i];

        const titleEl = item.querySelector("h3");
        const priceEl = item.querySelector(
          '[data-test-id="listing-card-price"]'
        );
        const linkEl = item.querySelector("a");
        const imageEl = item.querySelector("img");

        if (titleEl && linkEl) {
          results.push({
            platform: "etsy",
            platform_id: linkEl.href.split("/").pop(),
            title: titleEl.textContent.trim(),
            price: priceEl ? priceEl.textContent.trim() : "Price varies",
            url: linkEl.href,
            image: imageEl ? imageEl.src : null,
            location: "Etsy Marketplace",
            seller_info: JSON.stringify({ platform: "etsy" }),
          });
        }
      }

      return results;
    }, maxResults);

    console.log(`✅ Etsy: Found ${listings.length} listings`);
    return listings;
  } catch (error) {
    console.error(`❌ Etsy scraping error: ${error.message}`);
    return [];
  } finally {
    await browser.close();
  }
}

async function scrapeMercari(searchTerm, maxResults = 20) {
  console.log(`🔍 Mercari: Scraping for "${searchTerm}"`);

  const browser = await puppeteer.launch({ headless: "new" });

  try {
    const page = await browser.newPage();
    await page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    );

    const searchUrl = `https://www.mercari.com/search/?keyword=${encodeURIComponent(
      searchTerm
    )}`;
    await page.goto(searchUrl, {
      waitUntil: "domcontentloaded",
      timeout: 15000,
    });

    await page.waitForTimeout(3000);

    const listings = await page.evaluate((maxResults) => {
      const items = document.querySelectorAll(
        '[data-testid="SearchResults"] > div'
      );
      const results = [];

      for (let i = 0; i < Math.min(items.length, maxResults); i++) {
        const item = items[i];

        const titleEl = item.querySelector("p");
        const priceEl = item.querySelector('span[data-testid="Price"]');
        const linkEl = item.querySelector("a");
        const imageEl = item.querySelector("img");

        if (titleEl && linkEl) {
          results.push({
            platform: "mercari",
            platform_id: linkEl.href.split("/").pop(),
            title: titleEl.textContent.trim(),
            price: priceEl ? priceEl.textContent.trim() : "See listing",
            url: `https://www.mercari.com${linkEl.getAttribute("href")}`,
            image: imageEl ? imageEl.src : null,
            location: "Mercari",
            seller_info: JSON.stringify({ platform: "mercari" }),
          });
        }
      }

      return results;
    }, maxResults);

    console.log(`✅ Mercari: Found ${listings.length} listings`);
    return listings;
  } catch (error) {
    console.error(`❌ Mercari scraping error: ${error.message}`);
    return [];
  } finally {
    await browser.close();
  }
}

async function scrapeRubyLane(searchTerm, maxResults = 20) {
  console.log(`🔍 Ruby Lane: Scraping for "${searchTerm}"`);

  const browser = await puppeteer.launch({ headless: "new" });

  try {
    const page = await browser.newPage();
    await page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    );

    const searchUrl = `https://www.rubylane.com/search?q=${encodeURIComponent(
      searchTerm
    )}`;
    await page.goto(searchUrl, {
      waitUntil: "domcontentloaded",
      timeout: 15000,
    });

    await page.waitForTimeout(2000);

    const listings = await page.evaluate((maxResults) => {
      const items = document.querySelectorAll(".item-card");
      const results = [];

      for (let i = 0; i < Math.min(items.length, maxResults); i++) {
        const item = items[i];

        const titleEl = item.querySelector(".item-title");
        const priceEl = item.querySelector(".price");
        const linkEl = item.querySelector("a");
        const imageEl = item.querySelector("img");

        if (titleEl && linkEl) {
          results.push({
            platform: "ruby-lane",
            platform_id: linkEl.href.split("/").pop(),
            title: titleEl.textContent.trim(),
            price: priceEl ? priceEl.textContent.trim() : "Contact dealer",
            url: linkEl.href,
            image: imageEl ? imageEl.src : null,
            location: "Ruby Lane Antiques",
            seller_info: JSON.stringify({
              platform: "ruby-lane",
              type: "antique_dealer",
            }),
          });
        }
      }

      return results;
    }, maxResults);

    console.log(`✅ Ruby Lane: Found ${listings.length} listings`);
    return listings;
  } catch (error) {
    console.error(`❌ Ruby Lane scraping error: ${error.message}`);
    return [];
  } finally {
    await browser.close();
  }
}

// Wildlife keyword detection
function analyzeText(title, description = "") {
  const text = (title + " " + description).toLowerCase();
  let score = 0;
  const flags = [];

  // Check for wildlife keywords
  WILDLIFE_KEYWORDS.forEach((keyword) => {
    if (text.includes(keyword.toLowerCase())) {
      score += 3;
      flags.push(`Contains keyword: "${keyword}"`);
    }
  });

  // Additional suspicious patterns
  const patterns = [
    {
      regex: /\b(antique|vintage|old|ancient)\s+(bone|carved|carving)\b/i,
      score: 2,
      flag: "Antique bone/carving mention",
    },
    {
      regex: /\b(rare|exotic|illegal|banned)\b/i,
      score: 1,
      flag: "Suspicious descriptors",
    },
    {
      regex: /\b(africa|asia|safari|hunt|trophy)\b/i,
      score: 1,
      flag: "Geographic/hunting context",
    },
    {
      regex: /\b(authentic|genuine|real)\s+(ivory|horn|bone)\b/i,
      score: 3,
      flag: "Claims of authentic wildlife material",
    },
    {
      regex: /\b(estate|collection|inherited)\b/i,
      score: 1,
      flag: "Estate sale context",
    },
  ];

  patterns.forEach((pattern) => {
    if (pattern.regex.test(text)) {
      score += pattern.score;
      flags.push(pattern.flag);
    }
  });

  return {
    score: Math.min(score, 10),
    flags,
  };
}

// Image analysis with Claude Vision
async function analyzeImage(imageUrl, platform = "unknown") {
  if (!imageUrl || imageUrl.includes("placeholder")) {
    return {
      score: 2,
      analysis: "No real image available - score based on text analysis only.",
    };
  }

  try {
    console.log(
      `🔍 Analyzing image from ${platform}: ${imageUrl.substring(0, 80)}...`
    );

    const response = await anthropic.messages.create({
      model: "claude-3-sonnet-20240229",
      max_tokens: 350,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: `Analyze this image from ${platform} marketplace for potential illegal wildlife products.

ILLEGAL WILDLIFE MATERIALS TO DETECT:
- Ivory (elephant tusks, carved ivory objects) - cream/white with distinctive grain patterns
- Rhino horn (black/gray, curved horn material) - fibrous texture, often carved into cups
- Tiger parts (teeth, claws, bone, skin with orange/black stripes)
- Pangolin scales (overlapping brown armor-like scales)
- Turtle/tortoise shell (amber/brown patterned shell material)
- Coral (black coral jewelry, branching coral structures)
- Exotic skins (leopard spots, python patterns, crocodile texture)
- Carved bone items that might be from protected species

VISUAL CLUES TO LOOK FOR:
- Natural grain patterns characteristic of ivory
- Fibrous texture in horn materials
- Distinctive animal patterns (tiger stripes, leopard spots)
- Age/patina suggesting vintage animal products
- Carved animal motifs (elephants, rhinos) on suspicious materials
- Professional craftsmanship suggesting high-value wildlife products

Rate likelihood of illegal wildlife content (1-10):
1-3 = Unlikely (clearly synthetic, common materials)
4-6 = Possible (unclear materials, needs investigation)  
7-10 = Highly likely (strong indicators of real wildlife materials)

Format: SCORE: X/10
REASON: [specific visual evidence you observed]`,
            },
            {
              type: "image",
              source: {
                type: "url",
                url: imageUrl,
              },
            },
          ],
        },
      ],
    });

    const analysis = response.content[0].text;
    const scoreMatch = analysis.match(/SCORE:\s*(\d+)/i);
    const score = scoreMatch ? parseInt(scoreMatch[1]) : 3;

    console.log(`📊 Image analysis complete. Score: ${score}/10`);

    return {
      score,
      analysis,
    };
  } catch (error) {
    console.error(`❌ Error analyzing image: ${error.message}`);

    if (
      error.message.includes("401") ||
      error.message.includes("unauthorized")
    ) {
      console.error(
        `🔑 Anthropic API Key issue. Check ANTHROPIC_API_KEY and credits.`
      );
    }

    return {
      score: 1,
      analysis: `Image analysis failed: ${error.message}`,
    };
  }
}

// Process individual listing
async function processListing(listing) {
  console.log(
    `🔄 Processing ${listing.platform}: "${listing.title.substring(0, 50)}..."`
  );

  // Analyze text
  const textAnalysis = analyzeText(listing.title, listing.description);

  // Analyze image
  const imageAnalysis = await analyzeImage(listing.image, listing.platform);

  // Calculate weighted risk score (60% image, 40% text)
  const riskScore =
    Math.round((imageAnalysis.score * 0.6 + textAnalysis.score * 0.4) * 10) /
    10;

  // Combine flags
  const allFlags = [...textAnalysis.flags];
  if (imageAnalysis.score > 5) {
    allFlags.push("High-risk image detected");
  }
  if (listing.platform === "craigslist" && textAnalysis.score > 3) {
    allFlags.push("Craigslist posting - often used for illegal sales");
  }

  // Save to database
  return new Promise((resolve, reject) => {
    const stmt = db.prepare(`
      INSERT OR REPLACE INTO listings 
      (platform, platform_id, title, description, price, images, listing_url, location, 
       text_score, image_score, risk_score, flags, analysis_result, seller_info)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    stmt.run(
      [
        listing.platform,
        listing.platform_id,
        listing.title,
        listing.description || "",
        listing.price,
        JSON.stringify([listing.image]),
        listing.url,
        listing.location,
        textAnalysis.score,
        imageAnalysis.score,
        riskScore,
        JSON.stringify(allFlags),
        imageAnalysis.analysis,
        listing.seller_info || "{}",
      ],
      function (err) {
        if (err) reject(err);
        else {
          console.log(
            `✅ Saved ${listing.platform} listing (Risk: ${riskScore}/10)`
          );
          resolve(this.lastID);
        }
      }
    );

    stmt.finalize();
  });
}

// Main scanning function for all 3 platforms
async function scanAllPlatforms() {
  console.log("🚀 Starting 3-PLATFORM wildlife trade scan...\n");
  console.log("🎯 Platforms: Amazon + eBay + Craigslist\n");

  // Check configuration
  const ebayConfigured = !!(
    PLATFORM_CONFIG.ebay.clientId && PLATFORM_CONFIG.ebay.clientSecret
  );
  const amazonConfigured = !!(
    PLATFORM_CONFIG.amazon.accessKey && PLATFORM_CONFIG.amazon.secretKey
  );

  console.log("📋 Platform Status:");
  console.log(
    `  eBay API: ${ebayConfigured ? "✅ Configured" : "❌ Missing credentials"}`
  );
  console.log(
    `  Amazon API: ${
      amazonConfigured ? "✅ Configured" : "❌ Missing credentials"
    }`
  );
  console.log(`  Craigslist: ✅ Scraping enabled`);
  console.log("");

  const searchTerms = [
    "antique ivory",
    "vintage bone carving",
    "scrimshaw",
    "tiger tooth",
    "rhino horn",
  ];

  let totalProcessed = 0;
  let totalErrors = 0;
  const MAX_ITEMS = 30; // Reasonable limit for testing

  // Collect all search promises
  // Updated scanAllPlatforms with more platforms
  const searchPromises = [];

  // eBay (if configured)
  if (ebayConfigured) {
    searchTerms.forEach((term) => {
      searchPromises.push(searchEbayAPI(term, 8));
    });
  }

  // Craigslist
  searchTerms.forEach((term) => {
    searchPromises.push(scrapeCraigslist(term, 6));
  });

  // Etsy
  searchTerms.forEach((term) => {
    searchPromises.push(scrapeEtsy(term, 6));
  });

  // Mercari
  searchTerms.forEach((term) => {
    searchPromises.push(scrapeMercari(term, 6));
  });

  // Ruby Lane (high-value antiques)
  searchTerms.forEach((term) => {
    searchPromises.push(scrapeRubyLane(term, 4));
  });

  console.log(
    `🔄 Executing ${searchPromises.length} searches across all platforms...`
  );

  // Execute all searches concurrently
  const searchResults = await Promise.allSettled(searchPromises);

  // Flatten and deduplicate results
  const allListings = searchResults
    .filter((result) => result.status === "fulfilled")
    .flatMap((result) => result.value)
    .slice(0, MAX_ITEMS);

  // Remove duplicates based on title similarity
  const uniqueListings = [];
  for (const listing of allListings) {
    const isDuplicate = uniqueListings.some(
      (existing) =>
        listing.title
          .toLowerCase()
          .includes(existing.title.toLowerCase().substring(0, 30)) ||
        existing.title
          .toLowerCase()
          .includes(listing.title.toLowerCase().substring(0, 30))
    );
    if (!isDuplicate) {
      uniqueListings.push(listing);
    }
  }

  console.log(
    `\n💰 Processing ${uniqueListings.length} unique listings (API cost: ~$${(
      uniqueListings.length * 0.03
    ).toFixed(2)})`
  );
  console.log(`🔄 Starting AI analysis of each listing...\n`);

  // Process each listing with AI analysis
  for (const listing of uniqueListings) {
    try {
      await processListing(listing);
      totalProcessed++;

      // Rate limiting between API calls
      await new Promise((resolve) => setTimeout(resolve, 3000));
    } catch (error) {
      console.error(
        `❌ Error processing ${listing.platform} listing: ${error.message}`
      );
      totalErrors++;

      if (
        error.message.includes("401") ||
        error.message.includes("unauthorized")
      ) {
        console.error(`🔑 API Authentication issue detected`);
        break;
      }
    }
  }

  // Generate platform statistics
  const platformStats = {};
  uniqueListings.forEach((listing) => {
    platformStats[listing.platform] =
      (platformStats[listing.platform] || 0) + 1;
  });

  console.log(`\n🎉 3-PLATFORM SCAN COMPLETE!`);
  console.log(
    `📊 Results: ${totalProcessed} listings processed, ${totalErrors} errors`
  );
  console.log(`🌍 Platform breakdown:`);
  Object.entries(platformStats).forEach(([platform, count]) => {
    console.log(`  ${platform}: ${count} listings`);
  });
  console.log(`💰 Total API cost: ~$${(totalProcessed * 0.03).toFixed(2)}`);
  console.log(`🌐 View results at: http://localhost:3000`);

  // Query high-risk items
  const highRiskQuery =
    "SELECT COUNT(*) as count FROM listings WHERE risk_score >= 7";
  db.get(highRiskQuery, [], (err, row) => {
    if (!err && row.count > 0) {
      console.log(
        `\n🚨 ALERT: ${row.count} HIGH-RISK items detected (score 7-10)!`
      );
      console.log(
        `📱 Check dashboard immediately for potential wildlife violations`
      );
    }
  });

  return {
    totalProcessed,
    platformStats,
    uniqueListings: uniqueListings.length,
  };
}

// Express server for dashboard
const app = express();
app.use(express.static("public"));
app.use(express.json());

// Enhanced API endpoints
app.get("/api/listings", (req, res) => {
  const { platform, riskLevel } = req.query;

  let query = "SELECT * FROM listings WHERE 1=1";
  const params = [];

  if (platform && platform !== "all") {
    query += " AND platform = ?";
    params.push(platform);
  }

  if (riskLevel === "high") {
    query += " AND risk_score >= 7";
  } else if (riskLevel === "medium") {
    query += " AND risk_score >= 4 AND risk_score < 7";
  } else if (riskLevel === "low") {
    query += " AND risk_score < 4";
  }

  query += " ORDER BY risk_score DESC, scraped_at DESC LIMIT 100";

  db.all(query, params, (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(
        rows.map((row) => ({
          ...row,
          images: JSON.parse(row.images || "[]"),
          flags: JSON.parse(row.flags || "[]"),
          seller_info: JSON.parse(row.seller_info || "{}"),
        }))
      );
    }
  });
});

app.get("/api/stats", (req, res) => {
  const queries = {
    total: "SELECT COUNT(*) as count FROM listings",
    highRisk: "SELECT COUNT(*) as count FROM listings WHERE risk_score >= 7",
    mediumRisk:
      "SELECT COUNT(*) as count FROM listings WHERE risk_score >= 4 AND risk_score < 7",
    lowRisk: "SELECT COUNT(*) as count FROM listings WHERE risk_score < 4",
    platforms:
      "SELECT platform, COUNT(*) as count FROM listings GROUP BY platform",
    recent:
      'SELECT COUNT(*) as count FROM listings WHERE scraped_at > datetime("now", "-24 hours")',
    avgRiskScore: "SELECT AVG(risk_score) as avg FROM listings",
  };

  const stats = {};
  let completed = 0;
  const totalQueries = Object.keys(queries).length;

  Object.entries(queries).forEach(([key, query]) => {
    if (key === "platforms") {
      db.all(query, [], (err, rows) => {
        if (!err) {
          stats[key] = rows.reduce((acc, row) => {
            acc[row.platform] = row.count;
            return acc;
          }, {});
        }
        completed++;
        if (completed === totalQueries) {
          res.json(stats);
        }
      });
    } else {
      db.get(query, [], (err, row) => {
        if (!err) {
          stats[key] =
            key === "avgRiskScore"
              ? Math.round((row.avg || 0) * 10) / 10
              : row.count || row.avg || 0;
        }
        completed++;
        if (completed === totalQueries) {
          res.json(stats);
        }
      });
    }
  });
});

// Manual scan trigger endpoint
app.post("/api/scan", async (req, res) => {
  try {
    console.log("🚀 Manual scan triggered from dashboard...");
    const results = await scanAllPlatforms();
    res.json({
      success: true,
      message: "Scan completed successfully",
      results,
    });
  } catch (error) {
    console.error("❌ Manual scan failed:", error);
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

// eBay webhook endpoint
app.post("/webhooks/ebay-notifications", express.json(), (req, res) => {
  console.log("eBay notification received:", req.body);

  // Handle verification challenge
  if (req.body.challenge_code) {
    return res.json({
      challengeResponse: req.body.challenge_code,
    });
  }

  res.status(200).json({ status: "received" });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(
    `🌐 3-Platform Wildlife Detector running at http://localhost:${PORT}`
  );
});

// Auto-run scan if this file is executed directly
if (require.main === module) {
  console.log("🎯 3-Platform Wildlife Trade Detector Starting...\n");

  // Check environment variables
  const requiredEnvVars = [
    "ANTHROPIC_API_KEY",
    "EBAY_CLIENT_ID",
    "EBAY_CLIENT_SECRET",
  ];

  const missingVars = requiredEnvVars.filter(
    (varName) => !process.env[varName]
  );

  if (missingVars.length > 0) {
    console.error("❌ Missing required environment variables:");
    missingVars.forEach((varName) => console.error(`  - ${varName}`));
    console.error("\nPlease set these variables before running the scanner.\n");
  }

  if (process.env.ANTHROPIC_API_KEY && process.env.EBAY_CLIENT_ID) {
    scanAllPlatforms().catch(console.error);
  }
}

module.exports = {
  searchEbayAPI,
  searchAmazonAPI,
  scrapeCraigslist,
  scrapeEtsy,
  scraperMercari,
  scanAllPlatforms,
  analyzeText,
  analyzeImage,
  processListing,
};
