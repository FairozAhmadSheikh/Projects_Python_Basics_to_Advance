# pip install pandas scikit-learn xgboost pefile

import pefile
import os

def extract_features(file_path):
    try:
        pe = pefile.PE(file_path)
        features = {
            'SizeOfCode': pe.OPTIONAL_HEADER.SizeOfCode,
            'SizeOfInitializedData': pe.OPTIONAL_HEADER.SizeOfInitializedData,
            'SizeOfUninitializedData': pe.OPTIONAL_HEADER.SizeOfUninitializedData,
            'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            'BaseOfCode': pe.OPTIONAL_HEADER.BaseOfCode,
            'ImageBase': pe.OPTIONAL_HEADER.ImageBase,
            'Subsystem': pe.OPTIONAL_HEADER.Subsystem,
            'DllCharacteristics': pe.OPTIONAL_HEADER.DllCharacteristics,
            'SizeOfImage': pe.OPTIONAL_HEADER.SizeOfImage,
            'NumberOfSections': len(pe.sections)
        }
        return features
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None