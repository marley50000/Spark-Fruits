-- Run this script in your Supabase SQL Editor to add the missing columns 
-- required for Rider Vehicle details (Plate Number & Color).

ALTER TABLE public.riders 
ADD COLUMN IF NOT EXISTS plate_number text,
ADD COLUMN IF NOT EXISTS vehicle_color text DEFAULT 'Green';
