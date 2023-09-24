import cv2
import pytesseract
import re

# Path to the Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load an image of the Aadhaar card
# Replace 'khushi.jpeg' with the path to your Aadhaar card image
image_path = 'test case/test1.jpg'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load the image.")
    exit()

# Preprocess the image (resize, grayscale, and thresholding)
image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Perform OCR using Tesseract
aadhaar_data = pytesseract.image_to_string(thresholded)

# Define a regular expression pattern for Date of Birth (DOB)
dob_pattern = r"DOB[:\s]*([\d/:-]+)"


# Extract DOB
dob_match = re.search(dob_pattern, aadhaar_data, re.IGNORECASE)
if dob_match:
    dob = dob_match.group(1).strip()
    print("DOB:", dob)
else:
    print("Date of birth not found in the Aadhaar card.")

# Define regular expressions for extracting other information (Name, Age, Aadhar Number)
name_pattern = r"Name[:\s]+([^\n]+)"
aadhar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

# Extract Name
name_match = re.search(name_pattern, aadhaar_data, re.IGNORECASE | re.DOTALL)
if name_match:
    name = name_match.group(1).strip()
    print("Name:", name)
else:
    print("Name not found in the Aadhaar card.")


# Extract Aadhar Number
aadhar_match = re.search(aadhar_pattern, aadhaar_data)
if aadhar_match:
    aadhar = aadhar_match.group().replace(" ", "")
    print("Aadhar Number:", aadhar)
else:
    print("Aadhar Number not found in the Aadhaar card.")


    # Save data to a text file
with open("data.txt", "w") as file:
    file.write(f"Aadhar Number is: {aadhar}\n")
    file.write(f"Date of Birth is: {dob}\n")
    print("Data saved to 'data.txt'")


# Release resources
cv2.destroyAllWindows()