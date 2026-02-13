-- OPTION 1: FIX THE TRIGGER (Recommended)
-- This creates a 'public.profiles' table and ensures the trigger works correctly.
-- Use this if you want to store user details like names/phones in the future.

-- 1. Create profiles table if not exists
create table if not exists public.profiles (
  id uuid references auth.users on delete cascade not null primary key,
  email text,
  full_name text,
  updated_at timestamp with time zone,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Enable RLS
alter table public.profiles enable row level security;

-- 3. Create policies
create policy "Public profiles are viewable by everyone." on public.profiles for select using (true);
create policy "Users can insert their own profile." on public.profiles for insert with check (auth.uid() = id);
create policy "Users can update own profile." on public.profiles for update using (auth.uid() = id);

-- 4. Create or Replace the Trigger Function
create or replace function public.handle_new_user() 
returns trigger as $$
begin
  insert into public.profiles (id, email, full_name)
  values (new.id, new.email, new.raw_user_meta_data->>'full_name');
  return new;
end;
$$ language plpgsql security definer;

-- 5. Drop existing trigger to avoid duplicates/errors
drop trigger if exists on_auth_user_created on auth.users;

-- 6. Re-create the trigger
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();


-- OPTION 2: REMOVE THE TRIGGER (If you just want Sign Up to work without profiles)
-- Uncomment the lines below and run ONLY these lines if Option 1 doesn't work or you don't need profiles.
/*
drop trigger if exists on_auth_user_created on auth.users;
drop function if exists public.handle_new_user();
*/
