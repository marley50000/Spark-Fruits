-- MASTER SETUP SCRIPT
-- Run this in your Supabase SQL Editor to fully set up the Rider System and fix all issues.

-- 1. Ensure 'orders' table has necessary columns
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='rider_id') THEN 
        ALTER TABLE public.orders ADD COLUMN rider_id uuid REFERENCES auth.users(id); 
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='rider') THEN 
        ALTER TABLE public.orders ADD COLUMN rider text; 
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='email') THEN 
        ALTER TABLE public.orders ADD COLUMN email text; 
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='payment_ref') THEN 
        ALTER TABLE public.orders ADD COLUMN payment_ref text; 
    END IF;
END $$;

-- 2. Create 'riders' table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.riders (
    id uuid REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    name text NOT NULL,
    phone text,
    vehicle_type text, -- 'Moto', 'Bicycle', 'Car'
    is_verified boolean DEFAULT false, 
    status text DEFAULT 'available', -- 'available', 'busy', 'offline'
    current_lat float,
    current_lng float,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Enable RLS on tables
ALTER TABLE public.riders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- 4. Rider Policies (Idempotent)
DROP POLICY IF EXISTS "Riders can see own data" ON public.riders;
CREATE POLICY "Riders can see own data" ON public.riders FOR SELECT USING (auth.uid() = id);

DROP POLICY IF EXISTS "Riders can update own status" ON public.riders;
CREATE POLICY "Riders can update own status" ON public.riders FOR UPDATE USING (auth.uid() = id);

DROP POLICY IF EXISTS "Public read riders" ON public.riders;
CREATE POLICY "Public read riders" ON public.riders FOR SELECT USING (true);

DROP POLICY IF EXISTS "Anyone can join as rider" ON public.riders;
CREATE POLICY "Anyone can join as rider" ON public.riders FOR INSERT WITH CHECK (auth.uid() = id);

-- 5. Order Policies (Fixing permissions)
DROP POLICY IF EXISTS "Enable insert for unauthenticated users" ON public.orders;
CREATE POLICY "Enable insert for unauthenticated users" ON public.orders FOR INSERT TO anon WITH CHECK (true);

DROP POLICY IF EXISTS "Enable insert for authenticated users" ON public.orders;
CREATE POLICY "Enable insert for authenticated users" ON public.orders FOR INSERT TO authenticated WITH CHECK (true);

-- Allow Riders to see available orders (MVP: All orders for now, or filter by status)
DROP POLICY IF EXISTS "Riders can view all orders" ON public.orders;
CREATE POLICY "Riders can view all orders" ON public.orders FOR SELECT TO authenticated USING (true);

DROP POLICY IF EXISTS "Riders can update orders" ON public.orders;
CREATE POLICY "Riders can update orders" ON public.orders FOR UPDATE TO authenticated USING (true); -- Ideally narrow this down

-- 6. Storage (Optional for images later)
-- insert storage setup here if needed
