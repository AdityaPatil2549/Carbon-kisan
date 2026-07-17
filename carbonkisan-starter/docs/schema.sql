-- =========================================
-- CarbonKisan — Full Schema + RLS Policies
-- Run this in the Supabase SQL Editor after project creation.
-- =========================================

create extension if not exists "uuid-ossp";

-- Drop existing tables to allow clean re-run
drop table if exists admin_audit_log cascade;
drop table if exists admins cascade;
drop table if exists certificates cascade;
drop table if exists transactions cascade;
drop table if exists buyers cascade;
drop table if exists listings cascade;
drop table if exists estimates cascade;
drop table if exists land_parcels cascade;
drop table if exists farmers cascade;
drop table if exists districts cascade;

create table districts (
  code               varchar(20) primary key,
  name               varchar(80) not null,
  soc_baseline       decimal(5,3),
  rainfall_zone      varchar(10) not null check (rainfall_zone in ('low','medium','high')),
  dominant_soil_type varchar(50) not null,
  soil_modifier      decimal(4,3) not null,
  verified           boolean not null default false  -- see backend/data/maharashtra_districts.csv header
);

create table farmers (
  id                  uuid primary key default uuid_generate_v4(),
  phone               varchar(15) unique not null,
  full_name           varchar(120) not null,
  district_code       varchar(20) references districts(code) not null,
  village             varchar(120),
  preferred_language  varchar(2) default 'mr' check (preferred_language in ('mr','hi','en')),
  profile_complete    boolean default false,
  created_at          timestamptz default now()
);

create table land_parcels (
  id             uuid primary key default uuid_generate_v4(),
  farmer_id      uuid references farmers(id) not null,
  area_ha        decimal(6,2) not null check (area_ha > 0),
  primary_crop   varchar(50) not null,
  soil_type      varchar(50) not null,
  district_code  varchar(20) references districts(code) not null,
  created_at     timestamptz default now()
);

create table estimates (
  id                uuid primary key default uuid_generate_v4(),
  farmer_id         uuid references farmers(id) not null,
  parcel_id         uuid references land_parcels(id),
  practice_type     varchar(30) not null check (practice_type in
                      ('no_till','cover_crop','no_till_cover_crop','agroforestry')),
  area_ha           decimal(6,2) not null,
  season_months     smallint not null check (season_months in (6,12)),
  co2e_tonnes       decimal(6,3) not null,
  confidence_low    decimal(6,3) not null,
  confidence_high   decimal(6,3) not null,
  inr_estimate      integer not null,
  shap_breakdown    jsonb not null,
  model_version     varchar(20) not null,
  created_at        timestamptz default now()
);

create table listings (
  id                 uuid primary key default uuid_generate_v4(),
  estimate_id        uuid references estimates(id) unique not null,
  farmer_id          uuid references farmers(id) not null,
  asking_price_inr   integer not null check (asking_price_inr > 0),
  status             varchar(20) default 'pending_verification' check (status in
                       ('pending_verification','live','sold','expired','rejected')),
  rejection_reason   text,
  published_at       timestamptz,
  expires_at         timestamptz not null default (now() + interval '90 days')
);

create table buyers (
  id             uuid primary key default uuid_generate_v4(),
  email          varchar(150) unique not null,
  org_name       varchar(150) not null,
  contact_name   varchar(120) not null,
  created_at     timestamptz default now()
);

create table transactions (
  id                     uuid primary key default uuid_generate_v4(),
  listing_id             uuid references listings(id) unique not null,
  buyer_id               uuid references buyers(id) not null,
  razorpay_payment_id    varchar(60) unique not null,
  amount_paid_inr        integer not null,
  platform_fee_inr       integer not null,
  farmer_payout_inr      integer not null,
  payout_status          varchar(20) default 'pending' check (payout_status in
                            ('pending','processing','completed','failed')),
  paid_at                timestamptz default now()
);

create table certificates (
  id                     uuid primary key default uuid_generate_v4(),
  transaction_id         uuid references transactions(id) unique not null,
  record_hash            varchar(64) not null,
  pdf_url                text not null,
  methodology_version    varchar(20) not null,
  status                 varchar(15) default 'active' check (status in ('active','superseded')),
  issued_at              timestamptz default now()
);

create table admins (
  id            uuid primary key default uuid_generate_v4(),
  email         varchar(150) unique not null,
  full_name     varchar(120) not null
);

create table admin_audit_log (
  id           uuid primary key default uuid_generate_v4(),
  admin_id     uuid references admins(id) not null,
  action       varchar(50) not null,
  target_id    uuid not null,
  reason       text,
  created_at   timestamptz default now()
);

-- =========================================
-- Row-Level Security
-- =========================================
alter table farmers enable row level security;
alter table land_parcels enable row level security;
alter table estimates enable row level security;
alter table listings enable row level security;
alter table transactions enable row level security;
alter table certificates enable row level security;

create policy farmer_self_select on farmers for select using (auth.uid()::text = id::text);
create policy farmer_self_update on farmers for update using (auth.uid()::text = id::text);

create policy parcel_owner_select on land_parcels for select using (auth.uid()::text = farmer_id::text);
create policy parcel_owner_insert on land_parcels for insert with check (auth.uid()::text = farmer_id::text);

create policy estimate_owner_select on estimates for select using (auth.uid()::text = farmer_id::text);

create policy listing_public_read on listings for select using (status = 'live' or auth.uid()::text = farmer_id::text);
create policy listing_owner_write on listings for update using (auth.uid()::text = farmer_id::text);

-- Transactions and certificates: NO client-side insert/update policy exists
-- for either table. That is deliberate, not an oversight — the backend's
-- service_role key (which bypasses RLS) is the only writer. Do not add a
-- client insert policy for these two tables.
create policy transaction_buyer_read on transactions for select using (auth.uid()::text = buyer_id::text);
create policy certificate_public_verify on certificates for select using (true);

-- Seed district reference data — see backend/data/maharashtra_districts.csv
-- for the full 36-district list with the honesty caveat on soil_modifier values.
-- Import that CSV via Supabase's table editor "Import data from CSV" feature
-- rather than retyping it here.
