-- RUN THIS IN YOUR SUPABASE SQL EDITOR TO FIX ORDER TRACKING --

-- Add 'email' column to orders table so users can see their own orders
ALTER TABLE public.orders ADD COLUMN email text;

-- (Optional) Add index for faster lookups by email
CREATE INDEX idx_orders_email ON public.orders(email);
