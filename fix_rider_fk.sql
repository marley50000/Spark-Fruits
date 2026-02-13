-- FIX RIDER FOREIGN KEY --

-- The error 'Key (id)=(...) is not present in table "users".' suggests the riders table 
-- is referencing 'public.users' instead of 'auth.users'.
-- We need to drop that constraint and point it to the correct auth table.

ALTER TABLE public.riders
  DROP CONSTRAINT IF EXISTS riders_id_fkey;

-- Re-add constraint pointing to auth.users
ALTER TABLE public.riders
  ADD CONSTRAINT riders_id_fkey
  FOREIGN KEY (id)
  REFERENCES auth.users (id)
  ON DELETE CASCADE;

-- Just in case there is a referencing to public.users (which might trigger the error if public.users is expected)
-- We ensure we are referencing auth.users.
