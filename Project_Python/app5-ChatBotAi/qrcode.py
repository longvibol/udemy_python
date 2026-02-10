import pyqrcode
from PIL import Image

# Create a QR code object with the text "Hello, World!"
qr = pyqrcode.create("Hello, World!")

# Save the QR code as a PNG image
qr.png('hello_world_qr_code.png', scale=6)

print("QR code saved to hello_world_qr_code.png")