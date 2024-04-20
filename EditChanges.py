import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np


def get_shirt_measurements(image_path, reference_length=None):
 """
 This function attempts to measure the width and height of a shirt in an image
 using color segmentation and basic filtering.

 Args:
   image_path: Path to the image file.
   reference_length: Optional, length of a known object (in pixels) in the image
             for real-world unit conversion (defaults to None).

 Returns:
   A tuple containing the width and height of the shirt in pixels,
   or None if no shirt is detected. Additionally, a placeholder string
   indicating "Clothing Type: Unknown" is returned, and a boolean flag
   indicating whether a shirt was detected.
 """

 # Read the image
 img = cv2.imread(image_path)

 # Convert to RGB for color processing (if needed)
 img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 print(img_rgb)

 # Define color thresholds (adjust based on your target shirt color)
 lower_blue = np.array([100, 60, 0])
 upper_blue = np.array([37, 150, 190])

 # Create a mask to isolate pixels within the threshold range
 mask = cv2.inRange(img_rgb, lower_blue, upper_blue)

 # Apply opening and closing to remove noise (optional)
 kernel = np.ones((5, 5), np.uint8)
 mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
 mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

 # Find contours
 contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

 # Filter contours based on area (optional)
 filtered_contours = []
 min_area = 1000 # Adjust minimum area threshold as needed
 for cnt in contours:
  area = cv2.contourArea(cnt)
  if area > min_area:
   filtered_contours.append(cnt)

 # Detect largest contour (assuming single shirt)
 shirt_detected = False
 if len(filtered_contours) > 0:
  largest_contour = max(filtered_contours, key=cv2.contourArea)
  x, y, w, h = cv2.boundingRect(largest_contour)
  cv2.rectangle(img_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2) # Draw green rectangle
  shirt_detected = True
  width, height = w, h

 # Handle no shirt detection
 else:
  width, height = None, None

 # Placeholder for clothing type (replace with actual prediction in the future)
 clothing_type = "Unknown"

 if width and height:
  print(f"Shirt width: {width} pixels")
  if reference_length:
   # Assuming reference_length is in pixels, convert width to cm (adjust units as needed)
   width_cm = width * 1.0 / reference_length # Replace 1.0 with your conversion factor
   print(f"Estimated width (converted): {width_cm:.2f} cm")
  print(f"Shirt height: {height} pixels")
  if reference_length:
   # Assuming reference_length is in pixels, convert height to cm (adjust units as needed)
   height_cm = height * 1.0 / reference_length
   print(f"Estimated height (converted): {height_cm:.2f} cm")
 else:
  print("Shirt detection failed.")

 # Return measurements, clothing type placeholder, and detection flag
 return width, height, clothing_type, shirt_detected


def select_image():
 """Opens a file selection dialog and returns the chosen image path."""
 image_path = filedialog.askopenfilename(
   filetypes=[("Image Files", "*.jpg;*.png;*.gif")]
 )

 if image_path:
  # Get the reference length from user input (replace with your preferred method)


  def select_image():
    """Opens a file selection dialog and returns the chosen image path."""
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.png;*.gif")]
    )


  if image_path:
      reference_length_pixels = int(input("Enter reference length in pixels (optional): ")) if input("Do you have a reference length? (y/n): ").lower() == 'y' else None

      # Call the get_shirt_measurements function with the selected path and reference length
      width, height, clothing_type, shirt_detected = get_shirt_measurements(image_path, reference_length_pixels)

      print(f"Clothing Type: {clothing_type}")  # Print the clothing type placeholder

      # ... (Rest of your code for displaying the image or other actions)
  else:
      print("No image selected.")

# Create the main application window
root = tk.Tk()
root.title("Shirt Measurement Tool")

# Create a button to trigger the selection dialog
select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack()

# Run the main event loop for the GUI
root.mainloop()
