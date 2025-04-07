# ModularGrid Price Monitor - Troubleshooting Guide

This guide provides solutions to common issues you might encounter when using the ModularGrid Price Monitor.

## Authentication Issues

### Problem: "Authentication failed" error message

**Possible causes and solutions:**

1. **Incorrect credentials**
   - Double-check your username and password in the `config.json` file
   - Ensure there are no extra spaces before or after your username/password
   - Verify your credentials by logging in manually on the ModularGrid website

2. **Account issues**
   - Confirm your Unicorn account is active and not expired
   - Check if you can access price history when logged in manually

3. **Website changes**
   - ModularGrid may have updated their website structure
   - Check for updates to the ModularGrid Price Monitor

### Problem: Repeatedly asks for login

**Possible causes and solutions:**

1. **Session expiration**
   - This is normal behavior if the monitor runs for several days
   - The monitor will automatically attempt to re-authenticate

2. **Login page detection issue**
   - Check the logs for specific error messages
   - Try restarting the monitor

## Notification Issues

### Problem: Windows notifications not appearing

**Possible causes and solutions:**

1. **Notifications disabled in config**
   - Ensure `windows_enabled` is set to `true` in your `config.json`

2. **Windows notification settings**
   - Check Windows notification settings (Start > Settings > System > Notifications)
   - Make sure notifications are enabled for Python/command line applications
   - Try running the monitor as administrator

3. **Missing dependencies**
   - Reinstall the `win10toast` package:
     ```
     pip install win10toast --force-reinstall
     ```

### Problem: Email notifications not being sent

**Possible causes and solutions:**

1. **Email not configured correctly**
   - Verify `email_enabled` is set to `true` in your `config.json`
   - Check all SMTP settings are correct

2. **Email security settings**
   - For Gmail, ensure you're using an App Password, not your regular password
   - Check if your email provider blocks automated emails

3. **Network issues**
   - Verify your internet connection
   - Some networks block SMTP ports (especially corporate networks)

4. **Check spam folder**
   - Notifications might be delivered to your spam/junk folder

## Performance Issues

### Problem: High CPU usage

**Possible causes and solutions:**

1. **Too frequent scanning**
   - Increase the `scan_interval` value in your config
   - Recommended minimum: 1800 seconds (30 minutes)

2. **Too many regions selected**
   - Limit the regions you're monitoring to those you're interested in

### Problem: Program crashes or freezes

**Possible causes and solutions:**

1. **Memory issues**
   - Restart the monitor
   - If it happens regularly, try increasing the scan interval

2. **Database corruption**
   - Backup and delete the `modulargrid_monitor.db` file
   - The monitor will create a new database on next run

3. **Python environment issues**
   - Reinstall dependencies:
     ```
     pip install -r requirements.txt --force-reinstall
     ```

## Deal Detection Issues

### Problem: No deals being found

**Possible causes and solutions:**

1. **Threshold too high**
   - Lower the `default_threshold` value in your config
   - Try 10% instead of the default 15%

2. **No price history available**
   - Some modules might not have enough sales history
   - Check if you can see price history when logged in manually

3. **No new listings**
   - There might simply be no good deals at the moment
   - Be patient or adjust your threshold

### Problem: Too many deals/notifications

**Possible causes and solutions:**

1. **Threshold too low**
   - Increase the `default_threshold` value in your config

2. **Use digest mode**
   - Set `notification_frequency` to `digest` in your config

3. **Enable quiet hours**
   - Set `quiet_hours_enabled` to `true` and configure the hours

## Database Issues

### Problem: "Database is locked" error

**Possible causes and solutions:**

1. **Multiple instances running**
   - Ensure you're not running multiple instances of the monitor
   - Check Task Manager for multiple Python processes

2. **Database corruption**
   - Close the monitor
   - Make a backup of `modulargrid_monitor.db`
   - Delete the original file and restart the monitor

### Problem: Database growing too large

**Possible causes and solutions:**

1. **Long runtime**
   - This is normal if the monitor has been running for weeks/months
   - You can safely delete the database file to start fresh

2. **Excessive logging**
   - Edit the logging configuration in the Python files to reduce log level

## Network Issues

### Problem: "Connection refused" or timeout errors

**Possible causes and solutions:**

1. **Internet connection issues**
   - Check your internet connection
   - The monitor will automatically retry on next scan

2. **ModularGrid website down**
   - Check if you can access ModularGrid manually
   - Wait and the monitor will retry later

3. **Rate limiting**
   - If you're scanning too frequently, ModularGrid might block requests
   - Increase your scan interval

### Problem: Slow performance

**Possible causes and solutions:**

1. **Network latency**
   - This is normal and depends on your internet connection
   - Consider increasing the scan interval

2. **Too many regions**
   - Limit the regions you're monitoring

## Command Line Issues

### Problem: "Command not found" or similar errors

**Possible causes and solutions:**

1. **Python not in PATH**
   - Make sure Python is added to your system PATH
   - Try using the full path to Python:
     ```
     C:\Path\To\Python\python.exe modulargrid_monitor.py --monitor
     ```

2. **Wrong working directory**
   - Make sure you're in the correct directory when running commands
   - Use `cd` to navigate to the ModularGrid Price Monitor directory

### Problem: Command line window closes immediately

**Possible causes and solutions:**

1. **Error in script**
   - Run the command from an existing command prompt
   - Check the log files for errors

2. **Create a batch file**
   - Create a batch file with the following content:
     ```
     @echo on
     python modulargrid_monitor.py --monitor
     pause
     ```
   - This will keep the window open even if there's an error

## Advanced Troubleshooting

If you're experiencing issues not covered above:

1. **Check log files**
   - Review all log files in the ModularGrid Price Monitor directory
   - Look for ERROR or WARNING messages

2. **Enable debug logging**
   - Edit the Python files to change logging level to DEBUG
   - This will provide more detailed information

3. **Test components individually**
   - Test authentication:
     ```
     python modulargrid_monitor.py --test-login
     ```
   - Test marketplace access:
     ```
     python modulargrid_monitor.py --test-marketplace
     ```

4. **Check for updates**
   - Make sure you're using the latest version of the software

5. **Reinstall from scratch**
   - As a last resort, delete everything and reinstall following the setup guide

## Getting Help

If you've tried the solutions above and are still experiencing issues:

1. Collect all relevant log files
2. Note the exact steps that lead to the problem
3. Contact the developer with this information

Remember that the ModularGrid Price Monitor is designed to be robust and will automatically recover from most temporary issues on the next scan cycle.
