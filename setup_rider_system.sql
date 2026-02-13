-- RIDER SYSTEM SETUP

-- 1. Create a table for Riders to store their profile and status
CREATE TABLE IF NOT EXISTS public.riders (
    id uuid REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    name text NOT NULL,
    phone text,
    vehicle_type text, -- 'Moto', 'Bicycle', 'Car'
    is_verified boolean DEFAULT false, -- Admin must approve? Or auto-approve for now
    status text DEFAULT 'offline', -- 'available', 'busy', 'offline'
    current_lat float,
    current_lng float,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Update Orders table to support assignment
-- We already have 'rider' (text/name) and 'status'.
-- Let's add 'rider_id' for precise linking
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='rider_id') THEN 
        ALTER TABLE public.orders ADD COLUMN rider_id uuid REFERENCES auth.users(id); 
    END IF; 
END $$;

-- 3. RLS Policies for Riders
ALTER TABLE public.riders ENABLE ROW LEVEL SECURITY;

-- Allow riders to read/update their own data
DROP POLICY IF EXISTS "Riders can see own data" ON public.riders;
CREATE POLICY "Riders can see own data" ON public.riders FOR SELECT USING (auth.uid() = id);

DROP POLICY IF EXISTS "Riders can update own status" ON public.riders;
CREATE POLICY "Riders can update own status" ON public.riders FOR UPDATE USING (auth.uid() = id);

-- Allow public/admins to query riders (for assignment logic) - simplified for MVP
DROP POLICY IF EXISTS "Public read riders" ON public.riders;
CREATE POLICY "Public read riders" ON public.riders FOR SELECT USING (true);

-- Allow anyone to insert into riders (during signup)
DROP POLICY IF EXISTS "Enable insert for authenticated users only" ON public.riders; -- cleanup
DROP POLICY IF EXISTS "Anyone can join as rider" ON public.riders;
CREATE POLICY "Anyone can join as rider" ON public.riders FOR INSERT WITH CHECK (auth.uid() = id);
