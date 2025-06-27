-- WildGuard AI: Database Schema Updates for Enhanced System
-- Run these SQL commands in your Supabase SQL editor

-- Add new columns for enhanced threat detection
ALTER TABLE detections ADD COLUMN IF NOT EXISTS threat_category TEXT DEFAULT 'wildlife';
ALTER TABLE detections ADD COLUMN IF NOT EXISTS enhancement_notes TEXT;
ALTER TABLE detections ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(5,4) DEFAULT 0.0;
ALTER TABLE detections ADD COLUMN IF NOT EXISTS requires_human_review BOOLEAN DEFAULT FALSE;
ALTER TABLE detections ADD COLUMN IF NOT EXISTS vision_analyzed BOOLEAN DEFAULT FALSE;

-- Create index for filtering performance
CREATE INDEX IF NOT EXISTS idx_detections_threat_category ON detections(threat_category);
CREATE INDEX IF NOT EXISTS idx_detections_human_review ON detections(requires_human_review);

-- Update existing records based on status patterns (optional)
UPDATE detections 
SET threat_category = 'human' 
WHERE status LIKE '%HUMAN_TRAFFICKING%' 
   OR species_involved LIKE '%HUMAN_TRAFFICKING%'
   OR listing_title ILIKE '%massage%'
   OR listing_title ILIKE '%escort%'
   OR listing_title ILIKE '%young%';

-- Mark high-threat items for human review
UPDATE detections 
SET requires_human_review = TRUE 
WHERE threat_level = 'CRITICAL' 
   OR threat_score >= 85
   OR threat_category = 'human';

-- Verify the changes
SELECT 
    threat_category,
    COUNT(*) as count,
    AVG(threat_score) as avg_score
FROM detections 
GROUP BY threat_category
ORDER BY count DESC;

-- Check human review queue
SELECT 
    COUNT(*) as human_review_queue,
    threat_category
FROM detections 
WHERE requires_human_review = TRUE
GROUP BY threat_category;

COMMENT ON COLUMN detections.threat_category IS 'wildlife, human, or both';
COMMENT ON COLUMN detections.enhancement_notes IS 'AI reasoning for threat assessment';
COMMENT ON COLUMN detections.confidence_score IS 'AI confidence in threat assessment (0-1)';
COMMENT ON COLUMN detections.requires_human_review IS 'Flags items needing human verification';
COMMENT ON COLUMN detections.vision_analyzed IS 'Whether Google Vision API was used';
