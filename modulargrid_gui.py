#!/usr/bin/env python3
"""
ModularGrid Price Monitor - GUI Version
--------------------------------------
This module provides a graphical user interface for the ModularGrid Price Monitor.
It wraps the core functionality in a user-friendly Tkinter interface.
"""

import os
import sys
import json
import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import time
from datetime import datetime

# Import core modules
from modulargrid_scraper import ModularGridScraper
from modulargrid_database import ModularGridDatabase
from price_analyzer import PriceAnalyzer
from notification_system import NotificationSystem
from modulargrid_monitor import ModularGridMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("modulargrid_gui.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("modulargrid_gui")

class RedirectText:
    """Class to redirect stdout to a tkinter Text widget."""
    
    def __init__(self, text_widget):
        """Initialize with a text widget."""
        self.text_widget = text_widget
        self.buffer = ""
    
    def write(self, string):
        """Write to the text widget."""
        self.buffer += string
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")
    
    def flush(self):
        """Flush the buffer."""
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, self.buffer)
        self.buffer = ""
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")

class ModularGridGUI(tk.Tk):
    """Main GUI class for ModularGrid Price Monitor."""
    
    def __init__(self):
        """Initialize the GUI."""
        super().__init__()
        
        # Set window properties
        self.title("ModularGrid Price Monitor")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Set icon
        # self.iconbitmap("icon.ico")  # Will be added later
        
        # Initialize variables
        self.monitor = None
        self.monitor_thread = None
        self.is_monitoring = False
        self.config_file = "config.json"
        self.db_path = "modulargrid_monitor.db"
        
        # Load configuration
        self.load_config()
        
        # Create GUI elements
        self.create_menu()
        self.create_notebook()
        self.create_status_bar()
        
        # Initialize monitor
        self.initialize_monitor()
        
        # Set up protocol for window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start with login check
        self.after(1000, self.check_login)
    
    def load_config(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                # Create default config
                self.config = {
                    "username": "",
                    "password": "",
                    "scan_interval": 3600,
                    "regions": ["EU", "USA", "Canada", "Australia", "Asia", "Africa", "South America"],
                    "default_threshold": 15.0,
                    "email_enabled": False,
                    "email_address": "",
                    "smtp_server": "",
                    "smtp_port": 587,
                    "smtp_username": "",
                    "smtp_password": "",
                    "from_address": "",
                    "windows_enabled": True,
                    "notification_frequency": "immediate",
                    "quiet_hours_enabled": False,
                    "quiet_hours_start": "22:00",
                    "quiet_hours_end": "08:00"
                }
                self.save_config()
            
            logger.info("Configuration loaded")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            self.config = {}
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Run Single Scan", command=self.run_single_scan)
        file_menu.add_command(label="Start Monitoring", command=self.start_monitoring)
        file_menu.add_command(label="Stop Monitoring", command=self.stop_monitoring)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Manage Watchlist", command=self.show_watchlist)
        tools_menu.add_command(label="View Deals", command=self.show_deals)
        tools_menu.add_separator()
        tools_menu.add_command(label="Clear Logs", command=self.clear_logs)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Account Settings", command=self.show_account_settings)
        settings_menu.add_command(label="Notification Settings", command=self.show_notification_settings)
        settings_menu.add_command(label="General Settings", command=self.show_general_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Manual", command=self.show_user_manual)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menubar)
    
    def create_notebook(self):
        """Create the notebook with tabs."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dashboard tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.create_dashboard()
        
        # Logs tab
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="Logs")
        self.create_logs_tab()
    
    def create_dashboard(self):
        """Create the dashboard tab."""
        # Status frame
        status_frame = ttk.LabelFrame(self.dashboard_frame, text="Status")
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Status indicators
        self.status_var = tk.StringVar(value="Not Running")
        status_label = ttk.Label(status_frame, text="Monitor Status:")
        status_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        status_value = ttk.Label(status_frame, textvariable=self.status_var, font=("TkDefaultFont", 10, "bold"))
        status_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.last_scan_var = tk.StringVar(value="Never")
        last_scan_label = ttk.Label(status_frame, text="Last Scan:")
        last_scan_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        last_scan_value = ttk.Label(status_frame, textvariable=self.last_scan_var)
        last_scan_value.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.next_scan_var = tk.StringVar(value="N/A")
        next_scan_label = ttk.Label(status_frame, text="Next Scan:")
        next_scan_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        next_scan_value = ttk.Label(status_frame, textvariable=self.next_scan_var)
        next_scan_value.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.deals_found_var = tk.StringVar(value="0")
        deals_found_label = ttk.Label(status_frame, text="Deals Found:")
        deals_found_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        deals_found_value = ttk.Label(status_frame, textvariable=self.deals_found_var, font=("TkDefaultFont", 10, "bold"))
        deals_found_value.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        self.login_status_var = tk.StringVar(value="Not Logged In")
        login_status_label = ttk.Label(status_frame, text="Login Status:")
        login_status_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        login_status_value = ttk.Label(status_frame, textvariable=self.login_status_var)
        login_status_value.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Add some padding
        for child in status_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)
        
        # Action buttons frame
        action_frame = ttk.Frame(self.dashboard_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Action buttons
        scan_button = ttk.Button(action_frame, text="Run Single Scan", command=self.run_single_scan)
        scan_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.monitor_button_text = tk.StringVar(value="Start Monitoring")
        self.monitor_button = ttk.Button(action_frame, textvariable=self.monitor_button_text, command=self.toggle_monitoring)
        self.monitor_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        view_deals_button = ttk.Button(action_frame, text="View Deals", command=self.show_deals)
        view_deals_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Recent activity frame
        activity_frame = ttk.LabelFrame(self.dashboard_frame, text="Recent Activity")
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Activity log
        self.activity_text = ScrolledText(activity_frame, height=10)
        self.activity_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.activity_text.configure(state="disabled")
        
        # Add initial message
        self.add_activity("Welcome to ModularGrid Price Monitor!")
        self.add_activity("Use the menu or buttons to start monitoring for deals.")
    
    def create_logs_tab(self):
        """Create the logs tab."""
        # Log viewer
        self.log_text = ScrolledText(self.logs_frame)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.configure(state="disabled")
        
        # Redirect stdout to log viewer
        self.stdout_redirect = RedirectText(self.log_text)
        sys.stdout = self.stdout_redirect
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def initialize_monitor(self):
        """Initialize the ModularGrid monitor."""
        try:
            self.db = ModularGridDatabase(self.db_path)
            self.scraper = ModularGridScraper(self.config_file)
            self.analyzer = PriceAnalyzer(self.db)
            self.notifier = NotificationSystem(self.db, self.config_file)
            self.monitor = ModularGridMonitor(self.config_file, self.db_path)
            
            logger.info("Monitor initialized")
            self.set_status("Monitor initialized")
        except Exception as e:
            logger.error(f"Error initializing monitor: {e}")
            messagebox.showerror("Error", f"Failed to initialize monitor: {e}")
    
    def check_login(self):
        """Check if login credentials are set and valid."""
        username = self.config.get("username", "")
        password = self.config.get("password", "")
        
        if not username or not password:
            self.login_status_var.set("Not Configured")
            self.add_activity("Please configure your ModularGrid account in Settings > Account Settings")
            return
        
        self.login_status_var.set("Checking...")
        self.set_status("Checking login credentials...")
        
        # Run login check in a separate thread
        threading.Thread(target=self._check_login_thread, daemon=True).start()
    
    def _check_login_thread(self):
        """Thread function for login check."""
        try:
            success = self.scraper.login(self.config.get("username", ""), self.config.get("password", ""))
            
            if success:
                self.login_status_var.set("Logged In")
                self.add_activity("Successfully logged in to ModularGrid")
                self.set_status("Login successful")
            else:
                self.login_status_var.set("Login Failed")
                self.add_activity("Failed to log in to ModularGrid. Please check your credentials.")
                self.set_status("Login failed")
        except Exception as e:
            logger.error(f"Error checking login: {e}")
            self.login_status_var.set("Error")
            self.add_activity(f"Error checking login: {e}")
            self.set_status("Login error")
    
    def run_single_scan(self):
        """Run a single scan."""
        if self.is_monitoring:
            messagebox.showinfo("Info", "Monitoring is already running. Stop monitoring to run a single scan.")
            return
        
        self.set_status("Running scan...")
        self.add_activity("Starting single scan...")
        
        # Run scan in a separate thread
        threading.Thread(target=self._run_scan_thread, daemon=True).start()
    
    def _run_scan_thread(self):
        """Thread function for running a scan."""
        try:
            # Check login first
            if not self.scraper.authenticated:
                self.add_activity("Not logged in. Attempting to log in...")
                success = self.scraper.login(self.config.get("username", ""), self.config.get("password", ""))
                
                if not success:
                    self.add_activity("Login failed. Cannot run scan.")
                    self.set_status("Login failed")
                    return
            
            # Run scan
            self.add_activity("Scanning marketplace...")
            num_listings, num_deals, num_notified = self.monitor.run_scan_cycle()
            
            # Update UI
            self.last_scan_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.deals_found_var.set(str(self.get_total_deals()))
            
            self.add_activity(f"Scan complete: {num_listings} listings, {num_deals} new deals, {num_notified} notifications")
            self.set_status("Scan complete")
        except Exception as e:
            logger.error(f"Error running scan: {e}")
            self.add_activity(f"Error running scan: {e}")
            self.set_status("Scan error")
    
    def start_monitoring(self):
        """Start continuous monitoring."""
        if self.is_monitoring:
            messagebox.showinfo("Info", "Monitoring is already running.")
            return
        
        # Check login first
        if not self.scraper.authenticated:
            self.add_activity("Not logged in. Attempting to log in...")
            success = self.scraper.login(self.config.get("username", ""), self.config.get("password", ""))

(Content truncated due to size limit. Use line ranges to read in chunks)