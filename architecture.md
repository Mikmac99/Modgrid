# ModularGrid Price Monitor - Architecture Design

## Overview
The ModularGrid Price Monitor is a Windows application that automatically monitors the ModularGrid marketplace for eurorack modules being sold at prices lower than their typical market value. It leverages the user's Unicorn account to access historical price data for comparison.

## System Components

### 1. Authentication Module
- **Purpose**: Securely handle user login to ModularGrid
- **Features**:
  - Store encrypted credentials locally
  - Maintain authenticated session
  - Handle session renewal when expired
  - Provide login status feedback

### 2. Data Collection Module
- **Purpose**: Retrieve marketplace listings and price history
- **Features**:
  - Scrape current marketplace listings
  - Extract module details (name, price, condition, seller, region)
  - Access historical price data via Unicorn account features
  - Handle pagination and listing updates

### 3. Database Module
- **Purpose**: Store and manage price history and user preferences
- **Components**:
  - SQLite database for local storage
  - Tables:
    - Modules (id, name, manufacturer, hp, type)
    - Listings (id, module_id, price, seller, region, condition, date_listed)
    - PriceHistory (module_id, price, date_sold)
    - UserPreferences (module_ids_to_watch, price_threshold, regions_to_monitor)

### 4. Price Analysis Module
- **Purpose**: Compare current prices with historical data
- **Features**:
  - Calculate average market price for each module
  - Determine price thresholds for "good deals"
  - Flag listings that meet user-defined criteria
  - Consider module condition in price evaluation

### 5. Notification System
- **Purpose**: Alert user when good deals are found
- **Features**:
  - Windows notifications
  - Email alerts (optional)
  - Detailed listing information in alerts
  - Direct links to ModularGrid listings

### 6. User Interface
- **Purpose**: Allow user configuration and display results
- **Components**:
  - Settings panel for credentials and preferences
  - Dashboard showing monitored modules
  - Deal history view
  - Manual scan trigger option

## Data Flow

1. **Authentication Flow**:
   - User provides ModularGrid credentials
   - System securely stores encrypted credentials
   - Authentication module logs in and maintains session

2. **Monitoring Flow**:
   - Scheduler triggers periodic scans (configurable frequency)
   - Data collection module retrieves current marketplace listings
   - Database module stores new listings and updates existing ones
   - Price analysis module compares prices with historical data
   - Notification system alerts user when good deals are found

3. **Configuration Flow**:
   - User sets preferences through UI
   - Database module stores preferences
   - Monitoring system adapts to new preferences

## Technical Stack

- **Language**: Python 3.x
- **Web Scraping**: Selenium or Beautiful Soup
- **Database**: SQLite
- **UI Framework**: PyQt or Tkinter
- **Scheduling**: Windows Task Scheduler
- **Security**: Cryptography library for credential encryption

## Security Considerations

- Credentials stored with encryption
- No data sent to external servers
- All processing done locally
- Option for manual authentication

## Deployment Strategy

- Standalone Windows executable created with PyInstaller
- Simple installer for first-time setup
- Configuration wizard for initial setup
- Automatic updates (optional feature for future)
