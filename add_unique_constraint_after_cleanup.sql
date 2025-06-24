
-- Add unique constraint to prevent future duplicates
-- Run this in your Supabase SQL Editor after cleanup

-- First, check if constraint already exists
DO $$ 
BEGIN
    -- Add unique constraint on listing_url
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_listing_url' 
        AND conrelid = 'detections'::regclass
    ) THEN
        ALTER TABLE detections 
        ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);
        RAISE NOTICE 'Added unique constraint on listing_url';
    ELSE
        RAISE NOTICE 'Unique constraint already exists';
    END IF;
    
    -- Create performance indexes
    CREATE INDEX IF NOT EXISTS idx_detections_listing_url 
    ON detections(listing_url);
    
    CREATE INDEX IF NOT EXISTS idx_detections_platform_timestamp 
    ON detections(platform, timestamp DESC);
    
    CREATE INDEX IF NOT EXISTS idx_detections_timestamp 
    ON detections(timestamp DESC);
    
    RAISE NOTICE 'Performance indexes created/verified';
END $$;

-- Verify the constraint was added
SELECT conname, contype 
FROM pg_constraint 
WHERE conrelid = 'detections'::regclass 
AND conname = 'unique_listing_url';
