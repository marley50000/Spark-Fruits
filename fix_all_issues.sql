-- RUN THIS SCRIPT TO FIX ALL MISSING COLUMNS AND POLICIES --

-- 1. Ensure 'email' column exists (if not already)
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='email') THEN 
        ALTER TABLE public.orders ADD COLUMN email text; 
    END IF; 
END $$;

-- 2. Ensure 'payment_ref' column exists (this was causing errors)
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='orders' AND column_name='payment_ref') THEN 
        ALTER TABLE public.orders ADD COLUMN payment_ref text; 
    END IF; 
END $$;

-- 3. Fix RLS Policies (Idempotent - won't error if already exists)
-- First, drop ensuring no conflicts
DROP POLICY IF EXISTS "Anyone can create orders." ON public.orders;
DROP POLICY IF EXISTS "Enable insert for unauthenticated users" ON public.orders;
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON public.orders;

-- Re-create them cleanly
CREATE POLICY "Enable insert for unauthenticated users" 
ON public.orders FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Enable insert for authenticated users" 
ON public.orders FOR INSERT TO authenticated WITH CHECK (true);

-- 4. Enable RLS
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
