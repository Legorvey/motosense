import smbus
import time
import json # ADDED: Required for JSON storage

bus = smbus.SMBus(1)
address = 0x53

bus.write_byte_data(address, 0x2D, 0x08)

def get_raw_data():
    data = bus.read_i2c_block_data(address, 0x32, 6)
    x = data[0] | (data[1] << 8)
    y = data[2] | (data[3] << 8)
    z = data[4] | (data[5] << 8)
    
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536
    return x, y, z

print("Keep sensor perfectly still. Calibrating in 3 seconds...")
time.sleep(3)

x_sum, y_sum, z_sum = 0, 0, 0
samples = 100

for _ in range(samples):
    x, y, z = get_raw_data()
    x_sum += x
    y_sum += y
    z_sum += z
    time.sleep(0.01)

# Calculate final offsets
x_offset = - (x_sum / samples) / 256
y_offset = - (y_sum / samples) / 256
z_offset = - ((z_sum / samples) / 256 - 1)

print(f"X Offset: {x_offset:.3f} g")
print(f"Y Offset: {y_offset:.3f} g")
print(f"Z Offset: {z_offset:.3f} g")

# ADDED: Save the offsets to a JSON file
calibration_data = {
    "x_offset": x_offset,
    "y_offset": y_offset,
    "z_offset": z_offset
}

with open("calibration.json", "w") as json_file:
    json.dump(calibration_data, json_file, indent=4)

print("SUCCESS: Calibration data saved to 'calibration.json'.")