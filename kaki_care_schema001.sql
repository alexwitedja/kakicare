-- KAKI Care Database Schema
-- Run this in Supabase SQL Editor
-- Safe to rerun - drops existing tables first

-- Drop tables if exist (order matters due to foreign keys)
DROP TABLE IF EXISTS wearables;
DROP TABLE IF EXISTS personal_info;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS metrics;
DROP TABLE IF EXISTS users;

-- 1. Users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER,
  disease_profile JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Metrics (daily user-inputted vitals)
CREATE TABLE metrics (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  readings JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);

-- 3. Documents (OCR-extracted PDFs)
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  document_name TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Personal Info (AI-extracted notable events from chat)
CREATE TABLE personal_info (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  extracted_info TEXT
);

-- 5. Medications (daily adherence tracking)
CREATE TABLE medications (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  taken JSONB,
  UNIQUE(user_id, date)
);

-- 6. Wearables (raw device data)
CREATE TABLE wearables (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  raw_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for better query performance
CREATE INDEX idx_metrics_user_date ON metrics(user_id, date DESC);
CREATE INDEX idx_medications_user_date ON medications(user_id, date DESC);
CREATE INDEX idx_wearables_user_created ON wearables(user_id, created_at DESC);
CREATE INDEX idx_personal_info_user_timestamp ON personal_info(user_id, timestamp DESC);
CREATE INDEX idx_documents_user ON documents(user_id);
