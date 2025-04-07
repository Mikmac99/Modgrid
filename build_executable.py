#!/usr/bin/env python3
"""
ModularGrid Price Monitor - PyInstaller Build Script
This script runs PyInstaller to create a Windows executable.
"""

import os
import sys
import subprocess
import platform

def main():
    """Main function to build the executable."""
    print("Building ModularGrid Price Monitor executable...")
    
    # Determine the current platform
    current_platform = platform.system()
    print(f"Current platform: {current_platform}")
    
    # PyInstaller command
    pyinstaller_cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'modulargrid_gui.spec'
    ]
    
    # Run PyInstaller
    print("Running PyInstaller...")
    result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
    
    # Check result
    if result.returncode == 0:
        print("PyInstaller completed successfully!")
        
        # Get the output directory
        dist_dir = os.path.join(os.getcwd(), 'dist')
        exe_path = os.path.join(dist_dir, 'ModularGridPriceMonitor.exe' if current_platform == 'Windows' else 'ModularGridPriceMonitor')
        
        if os.path.exists(exe_path):
            print(f"Executable created at: {exe_path}")
        else:
            print(f"Warning: Expected executable not found at {exe_path}")
            
        # List files in dist directory
        print("\nFiles in dist directory:")
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                print(f"  {os.path.join(root, file)}")
    else:
        print("PyInstaller failed with the following error:")
        print(result.stderr)
        
        # Print more detailed error information
        print("\nStandard output:")
        print(result.stdout)
        
        sys.exit(1)
    
    print("\nBuild process completed!")

if __name__ == "__main__":
    main()
