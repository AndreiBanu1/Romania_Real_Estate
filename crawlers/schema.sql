CREATE TABLE agencies (
    id SERIAL PRIMARY KEY,
    external_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    type TEXT
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    city TEXT,
    province TEXT NOT NULL,
    neighborhood TEXT
);

CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT NOT NULL,
    property_url TEXT NOT NULL,  -- Stores the full URL
    estate_type TEXT,
    transaction_type TEXT,
    city TEXT,
    province TEXT,
    price NUMERIC,
    currency TEXT,
    price_per_sqm NUMERIC,
    area NUMERIC,
    rooms TEXT,
    floor TEXT,
    short_description TEXT,
    agency_id INT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_slug UNIQUE (slug)
);

CREATE TABLE property_images (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    medium_url TEXT NOT NULL,
    large_url TEXT NOT NULL
);

-- Indexes for faster searches
CREATE INDEX idx_properties_external_id ON properties (id);
CREATE INDEX idx_properties_city ON properties (city);
CREATE INDEX idx_properties_transaction_type ON properties (transaction_type);
CREATE INDEX idx_properties_price ON properties (price);

-- Index on images for quick retrieval
CREATE INDEX idx_property_images_property_id ON property_images (property_id);

-- TRIGGER FUNCTION TO GENERATE PROPERTY URL
CREATE OR REPLACE FUNCTION generate_property_url()
RETURNS TRIGGER AS $$
BEGIN
    NEW.property_url := 'https://www.storia.ro/ro/oferta/' || NEW.slug;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER TO AUTOMATICALLY GENERATE PROPERTY URL BEFORE INSERT OR UPDATE
CREATE TRIGGER before_insert_update_property_url
BEFORE INSERT OR UPDATE ON properties
FOR EACH ROW
EXECUTE FUNCTION generate_property_url();
