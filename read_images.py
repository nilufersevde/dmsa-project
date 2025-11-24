import os
import pydicom
import matplotlib
matplotlib.use("Agg")   # IMPORTANT: Agg backend = saves to file, no GUI needed
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

root = "/Users/nilufersevdeozdemir/Desktop/dmsa-hastalari" # patient folder

# Step 1 — read all DICOM files
dicoms = []
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        fpath = os.path.join(dirpath, fname)
        try:
            ds = pydicom.dcmread(fpath)
            dicoms.append(ds)
        except:
            pass

print("Total DICOM files:", len(dicoms))

# Step 2 — list all series
series = {}
for ds in dicoms:
    uid = getattr(ds, "SeriesInstanceUID", "UNKNOWN")
    if uid not in series:
        series[uid] = []
    series[uid].append(ds)

print("\nSeries found:")
for uid, items in series.items():
    arr = items[0].pixel_array
    desc = getattr(items[0], "SeriesDescription", "No Description")
    print(f"- {uid[:8]}... | {len(items)} files | shape={arr.shape} | {desc}")

# Step 3 — select the SPECT series
spect_ds = None
for ds in dicoms:
    desc = getattr(ds, "SeriesDescription", "").upper()
    if "SPECT" in desc:
        spect_ds = ds
        break

if spect_ds is None:
    print("\nNo SPECT series found.")
    exit()

print("\nSelected SPECT series:")
print("SeriesDescription:", spect_ds.SeriesDescription)

volume = spect_ds.pixel_array
print("SPECT volume shape:", volume.shape)  # (32, 64, 64)

# -----------------------------------------------------------
# SAVE ALL IMAGES TO FILE (no plt.show() so it works on macOS)
# -----------------------------------------------------------

# 1. First slice PNG
plt.figure(figsize=(5, 5))
plt.imshow(volume[0], cmap="gray")
plt.title("DMSA SPECT - first slice")
plt.axis("off")
plt.savefig("spect_first_slice.png", dpi=150)
plt.close()

# 2. All slices in grid
n = volume.shape[0]
cols = 8
rows = int(np.ceil(n / cols))

plt.figure(figsize=(12, 12))
for i in range(n):
    plt.subplot(rows, cols, i + 1)
    plt.imshow(volume[i], cmap="gray")
    plt.axis("off")
plt.suptitle("All SPECT Slices")
plt.tight_layout()
plt.savefig("spect_all_slices.png", dpi=150)
plt.close()

# 3. Smoothed slice
smoothed = gaussian_filter(volume, sigma=1.0)
plt.imshow(smoothed[0], cmap="gray")
plt.title("Smoothed Slice")
plt.axis("off")
plt.savefig("spect_smoothed_slice.png", dpi=150)
plt.close()

# 4. Normalized slice
v = volume.astype(float)
v = (v - v.min()) / (v.max() - v.min())

plt.imshow(v[0], cmap="gray")
plt.title("Normalized Slice")
plt.axis("off")
plt.savefig("spect_normalized_slice.png", dpi=150)
plt.close()

# 5. Intensity histogram
plt.hist(volume.flatten(), bins=100)
plt.title("Intensity Histogram")
plt.savefig("spect_histogram.png", dpi=150)
plt.close()

print("\nSaved PNGs:")
print(" - spect_first_slice.png")
print(" - spect_all_slices.png")
print(" - spect_smoothed_slice.png")
print(" - spect_normalized_slice.png")
print(" - spect_histogram.png")
