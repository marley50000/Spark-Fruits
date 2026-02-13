-- COMBINED RLS & FK FIXCRIPT (ROBUST VERSION) --

-- 1. Enable RLS on Essential Tables --
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.riders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

-- 2. ORDERS POLICIES --
DROP POLICY IF EXISTS "Anyone can create orders." ON public.orders;
DROP POLICY IF EXISTS "Enable insert for unauthenticated users" ON public.orders;
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON public.orders;
DROP POLICY IF EXISTS "Enable insert for all users" ON public.orders; 
DROP POLICY IF EXISTS "Authenticated users can view orders" ON public.orders;

CREATE POLICY "Enable insert for all users" 
ON public.orders 
FOR INSERT 
TO public 
WITH CHECK (true);

CREATE POLICY "Authenticated users can view orders" 
ON public.orders 
FOR SELECT 
TO authenticated 
USING (true);

-- 3. RIDERS POLICIES --
DROP POLICY IF EXISTS "Riders can see own data" ON public.riders;
DROP POLICY IF EXISTS "Public read riders" ON public.riders;
DROP POLICY IF EXISTS "Anyone can join as rider" ON public.riders;
DROP POLICY IF EXISTS "Authenticated users can join as rider" ON public.riders;
DROP POLICY IF EXISTS "Anon users can join as rider" ON public.riders;

CREATE POLICY "Riders can see own data" 
ON public.riders 
FOR SELECT 
TO authenticated 
USING (auth.uid() = id);

CREATE POLICY "Public read riders" 
ON public.riders 
FOR SELECT 
TO public 
USING (true);

CREATE POLICY "Authenticated users can join as rider" 
ON public.riders 
FOR INSERT 
TO authenticated 
WITH CHECK (auth.uid() = id);

-- FALLBACK: Allow ANON users to join as rider
CREATE POLICY "Anon users can join as rider" 
ON public.riders 
FOR INSERT 
TO anon 
WITH CHECK (true);

-- 4. PRODUCTS POLICIES --
DROP POLICY IF EXISTS "Public products are viewable by everyone." ON public.products;

CREATE POLICY "Public products are viewable by everyone." 
ON public.products 
FOR SELECT 
USING (true);

-- 5. FIX FOREIGN KEY (CRITICAL FOR SIGNUP) --
-- Drops the constraint referencing 'public.users' (if any) and points to 'auth.users'
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'riders_id_fkey' AND table_name = 'riders') THEN
    ALTER TABLE public.riders DROP CONSTRAINT riders_id_fkey;
  END IF;
END $$;

ALTER TABLE public.riders
  ADD CONSTRAINT riders_id_fkey
  FOREIGN KEY (id)
  REFERENCES auth.users (id)
  ON DELETE CASCADE;
