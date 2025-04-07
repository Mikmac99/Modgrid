# ModularGrid Price Monitor - User Manual

## Introduction

The ModularGrid Price Monitor is a powerful tool designed for eurorack enthusiasts who want to find great deals on modules. By leveraging your ModularGrid Unicorn account, this tool automatically monitors the marketplace for modules being sold below their typical market value and notifies you when good deals are found.

## Features

- **Automated Monitoring**: Continuously scans the ModularGrid marketplace for new listings
- **Price Analysis**: Compares current prices with historical data to identify good deals
- **Customizable Alerts**: Set your own thresholds for what constitutes a "good deal"
- **Multiple Notification Methods**: Receive alerts via Windows notifications or email
- **Region Filtering**: Focus on specific regions you're interested in
- **Watchlist**: Track specific modules you're looking to purchase
- **Quiet Hours**: Pause notifications during specified hours

## Getting Started

Before using the ModularGrid Price Monitor, make sure you have:

1. Installed the software following the instructions in the Setup Guide
2. Configured your settings in the `config.json` file
3. A valid ModularGrid Unicorn account

## Main Interface

The ModularGrid Price Monitor runs as a command-line application. While it doesn't have a graphical user interface, it's designed to be simple to use with straightforward commands.

## Commands Reference

### Basic Commands

- **Run continuous monitoring**:
  ```
  python modulargrid_monitor.py --monitor
  ```

- **Run a single scan**:
  ```
  python modulargrid_monitor.py --scan
  ```

- **Show help and available commands**:
  ```
  python modulargrid_monitor.py --help
  ```

### Watchlist Management

- **Add a module to watchlist**:
  ```
  python modulargrid_monitor.py --add-to-watchlist MODULE_ID [--threshold PERCENT] [--max-price AMOUNT]
  ```
  Example: `python modulargrid_monitor.py --add-to-watchlist 12345 --threshold 20 --max-price 300`

- **Show your watchlist**:
  ```
  python modulargrid_monitor.py --show-watchlist
  ```

- **Remove from watchlist**:
  ```
  python modulargrid_monitor.py --remove-from-watchlist MODULE_ID
  ```

### Configuration

- **Update configuration**:
  ```
  python modulargrid_monitor.py --update-config KEY VALUE
  ```
  Example: `python modulargrid_monitor.py --update-config scan_interval 1800`

- **Show current configuration**:
  ```
  python modulargrid_monitor.py --show-config
  ```

## Understanding Deal Detection

The ModularGrid Price Monitor uses several factors to determine if a listing is a good deal:

1. **Price Threshold**: The default is 15%, meaning a module must be listed at least 15% below its average historical price to be considered a deal.

2. **Maximum Price**: You can set a maximum price for modules in your watchlist. Even if a module is below the threshold percentage, it won't be flagged as a deal if it's above your maximum price.

3. **Condition**: The tool analyzes the condition description to adjust the deal score. Modules in excellent condition get a higher score than those with issues.

## Notification System

### Windows Notifications

When enabled, Windows notifications appear in the bottom right corner of your screen. These notifications include:
- Module name and manufacturer
- Current price and percentage below average
- Seller and region information

Clicking on a notification doesn't currently perform any action, but you can check the ModularGrid marketplace to find the listing.

### Email Notifications

Email notifications provide more detailed information:
- Module name and manufacturer
- Current price and average price
- Absolute and percentage savings
- Condition description
- Seller and region information
- Direct link to the listing

## Advanced Usage

### Customizing Scan Intervals

You can adjust how frequently the monitor checks for new listings by changing the `scan_interval` setting in your config file. The value is in seconds:
- 3600 = check every hour (default)
- 1800 = check every 30 minutes
- 7200 = check every 2 hours

### Setting Quiet Hours

If you don't want to be disturbed during certain hours:
1. Set `quiet_hours_enabled` to `true` in your config file
2. Set `quiet_hours_start` and `quiet_hours_end` to your preferred times (24-hour format)

During quiet hours, the monitor will still run and track deals, but won't send notifications until quiet hours are over.

### Notification Frequency

You can choose between two notification modes:
- `immediate`: Send a notification for each deal as it's found (default)
- `digest`: Group multiple deals into a single notification

Change this by setting `notification_frequency` in your config file.

## Data Storage

The ModularGrid Price Monitor stores all data in a SQLite database file named `modulargrid_monitor.db`. This includes:
- Module information
- Current and historical listings
- Price history
- Your watchlist and preferences

The database is automatically created and maintained by the software.

## Logs

The monitor creates several log files that can be useful for troubleshooting:
- `modulargrid_monitor.log`: Main application log
- `database.log`: Database operations
- `price_analysis.log`: Price comparison details
- `notifications.log`: Notification system activity

These logs are stored in the same directory as the application.

## Best Practices

For the best experience with ModularGrid Price Monitor:

1. **Run continuously**: The monitor works best when running continuously to catch new listings as they appear.

2. **Be selective with your watchlist**: Adding too many modules can make it harder to focus on the ones you really want.

3. **Adjust thresholds appropriately**: If you're getting too many notifications, increase your threshold. If you're not seeing any deals, decrease it.

4. **Check logs periodically**: The log files can provide insights into how the monitor is performing.

5. **Update regularly**: Check for updates to the software to get the latest features and bug fixes.

## Limitations

Please be aware of the following limitations:

1. The monitor can only access information that's available to your ModularGrid account. A Unicorn account is required to see price history.

2. The tool respects ModularGrid's servers by limiting request frequency. This means there may be a slight delay between a listing appearing on the site and the monitor detecting it.

3. Price analysis is based on historical data available on ModularGrid. For modules with limited sales history, the average price may not be fully representative.

4. The monitor cannot automatically purchase modules for you. You'll need to visit the ModularGrid marketplace to contact sellers.

## Privacy and Security

Your ModularGrid credentials are stored locally in the config file and are only used to authenticate with the ModularGrid website. The monitor does not share your information with any third parties.

For additional security:
- Keep your config.json file secure, as it contains your login credentials
- Consider using environment variables for sensitive information if running in a shared environment
