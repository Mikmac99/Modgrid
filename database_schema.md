# ModularGrid Price Monitor - Database Schema

## Overview
This document outlines the database schema for storing module listings, price history, and user preferences for the ModularGrid Price Monitor application.

## Tables

### 1. Modules
Stores information about eurorack modules.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| module_id | TEXT | ModularGrid's unique identifier for the module |
| name | TEXT | Module name |
| manufacturer | TEXT | Module manufacturer |
| hp | INTEGER | Module width in HP |
| type | TEXT | Module type/category |
| description | TEXT | Brief description of the module |

### 2. Listings
Stores current marketplace listings.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| listing_id | TEXT | ModularGrid's unique identifier for the listing |
| module_id | TEXT | Foreign key to Modules table |
| price | REAL | Listed price |
| currency | TEXT | Currency code (EUR, USD, etc.) |
| seller | TEXT | Seller username |
| region | TEXT | Geographic region |
| condition | TEXT | Condition description |
| date_listed | DATE | Date when the listing was posted |
| url | TEXT | Direct URL to the listing |
| last_checked | TIMESTAMP | When this listing was last verified |
| active | BOOLEAN | Whether the listing is still active |

### 3. PriceHistory
Stores historical price data for modules.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| module_id | TEXT | Foreign key to Modules table |
| price | REAL | Sold price |
| currency | TEXT | Currency code (EUR, USD, etc.) |
| date_sold | DATE | Date when the module was sold |
| condition | TEXT | Condition at time of sale (if available) |

### 4. UserPreferences
Stores user configuration and preferences.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| setting_name | TEXT | Name of the preference |
| setting_value | TEXT | Value of the preference |

### 5. WatchList
Stores modules the user wants to monitor.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| module_id | TEXT | Foreign key to Modules table |
| price_threshold | REAL | Price threshold for alerts (% below average) |
| max_price | REAL | Maximum price to consider (absolute value) |
| currency | TEXT | Currency code for max_price |
| notify | BOOLEAN | Whether to send notifications for this module |

### 6. Deals
Stores detected deals for historical tracking.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| listing_id | TEXT | Foreign key to Listings table |
| detected_date | TIMESTAMP | When the deal was detected |
| avg_price | REAL | Average price at time of detection |
| price_difference | REAL | Difference between listing price and average |
| percentage_below | REAL | Percentage below average price |
| notified | BOOLEAN | Whether user was notified about this deal |

## Indexes
- Modules(module_id)
- Listings(module_id)
- Listings(listing_id)
- PriceHistory(module_id)
- WatchList(module_id)

## Sample Queries

### Find Good Deals
```sql
SELECT l.*, m.name, m.manufacturer,
       (SELECT AVG(price) FROM PriceHistory WHERE module_id = l.module_id) as avg_price,
       (100 - (l.price / (SELECT AVG(price) FROM PriceHistory WHERE module_id = l.module_id) * 100)) as percent_below
FROM Listings l
JOIN Modules m ON l.module_id = m.module_id
JOIN WatchList w ON l.module_id = w.module_id
WHERE l.active = 1
  AND (100 - (l.price / (SELECT AVG(price) FROM PriceHistory WHERE module_id = l.module_id) * 100)) > w.price_threshold
  AND (w.max_price IS NULL OR l.price <= w.max_price)
ORDER BY percent_below DESC;
```

### Update Average Prices
```sql
SELECT module_id, AVG(price) as average_price
FROM PriceHistory
GROUP BY module_id;
```

### Find Recently Added Listings
```sql
SELECT l.*, m.name, m.manufacturer
FROM Listings l
JOIN Modules m ON l.module_id = m.module_id
WHERE l.date_listed > date('now', '-1 day')
ORDER BY l.date_listed DESC;
```
