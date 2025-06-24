-- WildGuard AI - Massive Duplicate Cleanup SQL
-- Run this in Supabase SQL Editor
-- Removes duplicates in batches of 10,000 with proper timeouts

-- Step 1: Create temporary table to identify duplicates to delete
-- This finds all duplicate records, keeping only the earliest one per URL

CREATE TEMP TABLE duplicates_to_delete AS
WITH ranked_detections AS (
  SELECT 
    id,
    listing_url,
    timestamp,
    ROW_NUMBER() OVER (
      PARTITION BY listing_url 
      ORDER BY timestamp ASC, id ASC
    ) as rn
  FROM detections 
  WHERE listing_url IS NOT NULL 
    AND listing_url != ''
)
SELECT id 
FROM ranked_detections 
WHERE rn > 1;

-- Check how many duplicates we found
SELECT COUNT(*) as duplicates_to_delete FROM duplicates_to_delete;

-- Step 2: Delete duplicates in batches of 10,000
-- Run this multiple times until it returns 0 rows deleted

DELETE FROM detections 
WHERE id IN (
  SELECT id 
  FROM duplicates_to_delete 
  LIMIT 10000
);

-- Check remaining duplicates after each batch
SELECT COUNT(*) as remaining_duplicates FROM duplicates_to_delete 
WHERE id NOT IN (SELECT id FROM detections);

-- Step 3: After all duplicates are deleted, add unique constraint
-- Run this ONLY after all duplicates are removed

-- First check if any duplicates remain:
SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT listing_url) as unique_urls,
  COUNT(*) - COUNT(DISTINCT listing_url) as remaining_duplicates
FROM detections;

-- If remaining_duplicates = 0, then add the constraint:
ALTER TABLE detections 
ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);

-- Create performance indexes
CREATE INDEX IF NOT EXISTS idx_detections_listing_url 
ON detections(listing_url);

CREATE INDEX IF NOT EXISTS idx_detections_platform_timestamp 
ON detections(platform, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_detections_timestamp 
ON detections(timestamp DESC);

-- Final verification
SELECT 
  COUNT(*) as final_total_records,
  COUNT(DISTINCT listing_url) as final_unique_urls,
  COUNT(*) - COUNT(DISTINCT listing_url) as final_duplicates
FROM detections;