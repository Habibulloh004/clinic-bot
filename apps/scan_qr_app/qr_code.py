import qrcode


def generate_phone_qr(phone_number, filename="phone_qr.png"):
    # Create the "tel:" link
    tel_link = f"tel:{phone_number}"

    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the phone link to the QR code
    qr.add_data(tel_link)
    qr.make(fit=True)

    # Create an image from the QR Code
    img = qr.make_image(fill="black", back_color="white")

    # Save the image
    img.save(filename)

    # Optionally show the image
    img.show()


if __name__ == "__main__":
    # Example phone number
    phone_number = "+998901234567"

    # Generate the QR code
    generate_phone_qr(phone_number)
