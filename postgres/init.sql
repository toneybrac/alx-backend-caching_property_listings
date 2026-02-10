-- postgres/init.sql
-- Initialize database with some sample data

-- Create extension if not exists (for PostgreSQL specific features)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create test data
INSERT INTO properties_property (title, description, price, location, created_at)
VALUES 
    ('Beautiful Beach House', 'Luxury beach house with ocean view', 500000.00, 'Miami, FL', NOW()),
    ('Downtown Apartment', 'Modern apartment in city center', 250000.00, 'New York, NY', NOW()),
    ('Mountain Cabin', 'Cozy cabin with mountain views', 150000.00, 'Denver, CO', NOW()),
    ('Suburban Family Home', 'Spacious home in quiet neighborhood', 350000.00, 'Austin, TX', NOW()),
    ('Luxury Penthouse', 'Penthouse with rooftop pool', 1000000.00, 'Los Angeles, CA', NOW())
ON CONFLICT DO NOTHING;
