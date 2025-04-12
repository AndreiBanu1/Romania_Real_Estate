import psycopg2
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "real_estate_db"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "admin"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        self.cursor = self.connection.cursor()

    def safe_get(self, data, keys, default=""):
        """Safely extract nested values, ensuring the final result is a string"""
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, {})
            else:
                return default
        return str(result) if isinstance(result, (str, int, float)) else default

    def insert_property(self, property_data):
        try:
            property_id = property_data.get("id")
            if property_id is None:
                raise ValueError("❌ Missing property ID")

            title = property_data.get("title", "Unknown Title")
            property_url = property_data.get("property_url", "")
            estate_type = property_data.get("estate", "NA")
            transaction_type = property_data.get("transaction", "NA")
            slug = property_data.get("slug") or re.sub(r'[^a-z0-9-]', '', title.lower().replace(" ", "-"))

            # ✅ Extracting location as plain text
            city = self.safe_get(property_data, ["location", "address", "city", "name"], "NA")
            province = self.safe_get(property_data, ["location", "address", "province", "name"], "NA")
            street_name = self.safe_get(property_data, ["location", "address", "street", "name"], "").strip()
            location = json.dumps({"street": street_name, "province": province}) if street_name or province else '"Unknown Location"'


            # ✅ Extracting numeric values
            price = self.safe_get(property_data, ["totalPrice", "value"], 0)
            price = float(price) if price else None  
            currency = self.safe_get(property_data, ["totalPrice", "currency"], "EUR")
            price_per_sqm = self.safe_get(property_data, ["pricePerSquareMeter", "value"], 0)
            price_per_sqm = float(price_per_sqm) if price_per_sqm else None  
            area = property_data.get("areaInSquareMeters", None)
            area = float(area) if area else None  
            rooms = property_data.get("roomsNumber", None)
            floor = property_data.get("floorNumber", None)
            short_description = property_data.get("shortDescription", "NA")

            # ✅ Extract agency details
            agency_id = self.safe_get(property_data, ["agency", "id"], None)
            agency_name = self.safe_get(property_data, ["agency", "name"], "NA")
            agency_slug = self.safe_get(property_data, ["agency", "slug"], "NA")

            # ✅ Convert JSON fields properly
            images_json = json.dumps(property_data.get("images", []))

            print(f"Trying to insert: agency_slug={agency_slug}, city={city}, street={street_name}, images_json={images_json}")

            # ✅ Insert into PostgreSQL
            sql_query = """
                INSERT INTO properties (id, title, slug, property_url, estate_type, transaction_type, city, province, price, 
                                        currency, price_per_sqm, area, rooms, floor, short_description, agency_id, 
                                        agency_name, agency_slug, location, images)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                ON CONFLICT (id) 
                DO UPDATE SET 
                    title = EXCLUDED.title,
                    slug = EXCLUDED.slug,
                    property_url = EXCLUDED.property_url,
                    estate_type = EXCLUDED.estate_type,
                    transaction_type = EXCLUDED.transaction_type,
                    city = EXCLUDED.city,
                    province = EXCLUDED.province,
                    price = EXCLUDED.price,
                    currency = EXCLUDED.currency,
                    price_per_sqm = EXCLUDED.price_per_sqm,
                    area = EXCLUDED.area,
                    rooms = EXCLUDED.rooms,
                    floor = EXCLUDED.floor,
                    short_description = EXCLUDED.short_description,
                    agency_id = EXCLUDED.agency_id,
                    agency_name = EXCLUDED.agency_name,
                    agency_slug = EXCLUDED.agency_slug,
                    location = EXCLUDED.location,
                    images = EXCLUDED.images
            """

            self.cursor.execute(sql_query, (
                int(property_id),  
                title,
                slug,
                property_url,
                estate_type,
                transaction_type,  
                city,
                province,
                price,  
                currency,
                price_per_sqm,  
                area,  
                rooms,
                floor,
                short_description,
                agency_id,  
                agency_name,
                agency_slug,
                location,
                images_json  
            ))

            print(f"✅ Inserted property: {title} (ID: {property_id})")
            self.connection.commit()
        except Exception as e:
            print(f"❌ Error inserting property: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()