-- Add missing columns to detections table
-- Run this in your Supabase SQL Editor

ALTER TABLE detections 
ADD COLUMN IF NOT EXISTS listing_title TEXT,
ADD COLUMN IF NOT EXISTS listing_url TEXT,
ADD COLUMN IF NOT EXISTS listing_price TEXT,
ADD COLUMN IF NOT EXISTS search_term TEXT;

-- Verify the new structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'detections' 
ORDER BY ordinal_position;
