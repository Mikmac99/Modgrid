import os
import sys
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# Create a simple icon for the ModularGrid Price Monitor
# This will be a stylized "MG" with a price tag

# Create a new image with a transparent background
img_size = 256
icon = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(icon)

# Define colors
primary_color = (76, 175, 80)  # Green
secondary_color = (33, 33, 33)  # Dark gray
accent_color = (255, 193, 7)    # Amber

# Draw a rounded rectangle background
draw.rectangle([(20, 20), (img_size-20, img_size-20)], 
               fill=primary_color, 
               outline=secondary_color, 
               width=8)

# Draw a price tag in the corner
tag_points = [
    (img_size-60, 20),  # Top left
    (img_size-20, 20),  # Top right
    (img_size-20, 60),  # Bottom right
    (img_size-80, 60),  # Bottom left
]
draw.polygon(tag_points, fill=accent_color, outline=secondary_color, width=3)

# Draw a hole in the price tag
draw.ellipse([(img_size-50, 30), (img_size-30, 50)], fill=(255, 255, 255, 180))

# Draw "MG" text
draw.text((60, 80), "MG", fill=secondary_color, width=15)
draw.text((60, 140), "MONITOR", fill=secondary_color, width=8)

# Draw a down arrow to represent price drop
arrow_points = [
    (128, 180),  # Top
    (158, 210),  # Bottom right
    (138, 210),  # Bottom middle right
    (138, 230),  # Middle bottom
    (118, 230),  # Middle bottom
    (118, 210),  # Bottom middle left
    (98, 210),   # Bottom left
]
draw.polygon(arrow_points, fill=accent_color, outline=secondary_color, width=3)

# Save the icon
icon.save('icon.png')

# Also save as ICO for Windows
icon.save('icon.ico', format='ICO')

print("Icon created successfully!")
