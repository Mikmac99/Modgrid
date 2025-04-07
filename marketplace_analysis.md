# ModularGrid Marketplace Analysis

## Website Structure
- ModularGrid marketplace is accessible at https://modulargrid.net/e/offers
- Listings are displayed in a tabular format with details like price, seller, region, and condition
- Individual module listings have more detailed information and seller contact options
- Unicorn account provides access to used price history (essential for price comparison)

## Authentication Requirements
- Login system is available at the top of the page
- Authentication will be required to:
  - Access Unicorn account features
  - View previously sold prices
  - Contact sellers

## Data Required for Price Monitoring
1. **Current listing data:**
   - Module name
   - Current price
   - Seller information
   - Region
   - Condition description
   - Date listed

2. **Historical price data:**
   - Previously sold prices (accessible via Unicorn account)
   - Average market price for each module

3. **User preferences:**
   - Modules of interest
   - Price threshold settings (% below average)
   - Region preferences

## Programmatic Access Strategy
To build an automated monitoring tool, we'll need to:

1. **Handle authentication:**
   - Implement secure login with the user's credentials
   - Maintain session cookies for authenticated requests

2. **Scrape marketplace data:**
   - Periodically fetch the marketplace page
   - Parse HTML to extract current listings
   - Access individual module pages for detailed information

3. **Access historical price data:**
   - Navigate to module detail pages
   - Extract previously sold prices (Unicorn account feature)
   - Calculate average prices and identify trends

4. **Implement price comparison logic:**
   - Compare current prices with historical averages
   - Flag listings that are below a certain threshold
   - Consider condition and region in the comparison

5. **Notification system:**
   - Alert user when good deals are found
   - Provide direct links to the listings
   - Include relevant details about the module and price comparison

## Technical Implementation Considerations
- **Web scraping library:** Beautiful Soup or Selenium for HTML parsing
- **Authentication handling:** Requests library with session management
- **Data storage:** SQLite database for historical price tracking
- **Scheduling:** Windows Task Scheduler for periodic checks
- **User interface:** Simple GUI or command-line interface with configuration options
- **Security:** Secure storage of user credentials
