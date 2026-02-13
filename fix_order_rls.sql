-- FIX ORDER INSERTION PERMISSIONS --

-- The previous policy: 
-- create policy "Anyone can create orders." on public.orders for insert with check (true);
-- MIGHT BE FAILING because default RLS blocks anon users if not explicitly allowed or if there's a conflict.

-- 1. Drop the existing insert policy to be safe and recreate it explicitly for anon role
DROP POLICY IF EXISTS "Anyone can create orders." ON public.orders;

-- 2. Create a new policy that explicitly allows the 'anon' role (public users) to insert
CREATE POLICY "Enable insert for unauthenticated users" 
ON public.orders 
FOR INSERT 
TO anon 
WITH CHECK (true);

-- 3. Also allow authenticated users just in case
CREATE POLICY "Enable insert for authenticated users" 
ON public.orders 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

-- 4. Ensure RLS is still enabled but configured correctly
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
