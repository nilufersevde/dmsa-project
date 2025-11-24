import os
import pydicom

root = "/Users/nilufersevdeozdemir/Desktop/dmsa-hastalari"

for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        fpath = os.path.join(dirpath, fname)

        try:
            ds = pydicom.dcmread(fpath)
        except Exception:
            continue   # skip non-DICOM files if any

        print("----------------------------------")
        print("File:", fname)
        print("Patient Name:", ds.get("PatientName", "N/A"))
        print("Study Date:", ds.get("StudyDate", "N/A"))
        print("Modality:", ds.get("Modality", "N/A"))
        print("Series Description:", ds.get("SeriesDescription", "N/A"))

        if hasattr(ds, "pixel_array"):
            print("Image shape:", ds.pixel_array.shape)
