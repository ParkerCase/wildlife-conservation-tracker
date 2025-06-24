-- WildGuard AI: Database Duplicate Prevention
-- Add unique constraint to prevent future duplicates

-- First, let's see current duplicate situation
SELECT 
    'BEFORE_CONSTRAINT' as stage,
    COUNT(*) as total_records,
    COUNT(DISTINCT listing_url) as unique_urls,
    COUNT(*) - COUNT(DISTINCT listing_url) as duplicates_remaining
FROM detections 
WHERE listing_url IS NOT NULL AND listing_url != '';

-- Add unique constraint (will fail if duplicates exist)
-- Run cleanup first if this fails
DO $$
BEGIN
    BEGIN
        ALTER TABLE detections ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);
        RAISE NOTICE '✅ Unique constraint added successfully';
    EXCEPTION 
        WHEN unique_violation THEN
            RAISE NOTICE '⚠️  Cannot add constraint: duplicates exist';
            RAISE NOTICE '💡 Run cleanup script first: python cleanup/fast_cleanup.py';
        WHEN duplicate_table THEN
            RAISE NOTICE '✅ Constraint already exists';
    END;
END $$;

-- Verify constraint was added
SELECT 
    conname as constraint_name,
    contype as constraint_type
FROM pg_constraint 
WHERE conrelid = 'detections'::regclass 
AND conname = 'unique_listing_url';

-- Create index for better performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_detections_listing_url 
ON detections(listing_url) WHERE listing_url IS NOT NULL;

-- Verify final state
SELECT 
    'AFTER_CONSTRAINT' as stage,
    COUNT(*) as total_records,
    COUNT(DISTINCT listing_url) as unique_urls,
    COUNT(*) - COUNT(DISTINCT listing_url) as duplicates_remaining
FROM detections 
WHERE listing_url IS NOT NULL AND listing_url != '';
