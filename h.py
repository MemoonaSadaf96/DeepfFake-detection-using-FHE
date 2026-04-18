# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from google.colab import files
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Upload the images
uploaded = files.upload()

# Load images (query image and baseline image)
def load_image(image_path):
    img = image.load_img(image_path, target_size=(256, 256))  # Resize to 256x256 for consistency
    img_array = image.img_to_array(img)
    return img_array / 255.0  # Normalize to [0, 1]

# Correct file paths after uploading
query_image_path = 'Memoona Picture.jpeg'  # Replace with your uploaded query image
baseline_image_path = 'Memoona Picture.jpeg'  # Replace with your uploaded baseline image

# Load the query and baseline images
query_img = load_image(query_image_path)
baseline_img = load_image(baseline_image_path)

# Compute deviation (difference between the query and baseline images)
deviation = np.abs(query_img - baseline_img)  # Absolute difference between pixel values

# Flatten the deviation to work with hexbin (for all three color channels)
deviation_flattened = deviation.reshape(-1, 3)  # Flatten image to pixels
deviation_red = deviation_flattened[:, 0]  # R (Red channel)
deviation_green = deviation_flattened[:, 1]  # G (Green channel)
deviation_blue = deviation_flattened[:, 2]  # B (Blue channel)

# -----------------------------------------------
# Step 1: Simulate Homomorphic Encryption with RSA
# -----------------------------------------------

# Generate RSA keys (public and private)
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# Encrypt the deviation data (Simulating "encryption" of feature values)
def encrypt_data(data, pub_key):
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    encrypted_data = [cipher_rsa.encrypt(str(value).encode()) for value in data]
    return encrypted_data

# Decrypt function to retrieve the original data
def decrypt_data(encrypted_data, priv_key):
    cipher_rsa = PKCS1_OAEP.new(priv_key)
    decrypted_data = [float(cipher_rsa.decrypt(encrypted_value).decode()) for encrypted_value in encrypted_data]
    return decrypted_data

# Encrypt the deviation values for R, G, B channels
encrypted_deviation_red = encrypt_data(deviation_red, public_key)
encrypted_deviation_green = encrypt_data(deviation_green, public_key)
encrypted_deviation_blue = encrypt_data(deviation_blue, public_key)

# -----------------------------------------------
# Step 2: Perform "Homomorphic" operation (here simple addition and subtraction on encrypted values)
# In a real FHE setting, you would apply operations directly on the encrypted data
# Here we simulate the concept of performing operations on encrypted data:
def homomorphic_addition(data1, data2):
    return [val1 + val2 for val1, val2 in zip(data1, data2)]

# Simulate adding deviations on encrypted data (this operation happens on encrypted data in a real FHE system)
encrypted_result_red_green = homomorphic_addition(encrypted_deviation_red, encrypted_deviation_green)

# -----------------------------------------------
# Step 3: Decrypt the result
# -----------------------------------------------
# Decrypt the result to verify correctness
decrypted_result_red_green = decrypt_data(encrypted_result_red_green, private_key)

# -----------------------------------------------
# Step 4: Visualize the results
# -----------------------------------------------
# Show the original and decrypted result heatmaps
plt.figure(figsize=(10, 7))

# Create a heatmap for the deviation of the original image
plt.subplot(1, 2, 1)
plt.imshow(deviation[:, :, 0], cmap='Reds', interpolation='nearest')
plt.title('Original Deviation (Red Channel)')

# Create a heatmap for the decrypted result of the simulated homomorphic addition
plt.subplot(1, 2, 2)
plt.imshow(np.array(decrypted_result_red_green).reshape(256, 256), cmap='Reds', interpolation='nearest')
plt.title('Decrypted Homomorphic Result')

plt.show()

# Print out a few results to verify
print("Original Deviation Red Channel: ", deviation_red[:5])  # Show first 5 values
print("Decrypted Homomorphic Result: ", decrypted_result_red_green[:5])  # Show first 5 values