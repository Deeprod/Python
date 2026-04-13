import os

def add_prefix_to_current_folder_files(prefix):
    current_folder = os.getcwd()

    for filename in os.listdir(current_folder):
        full_path = os.path.join(current_folder, filename)

        if os.path.isfile(full_path):
            new_name = prefix + filename
            new_full_path = os.path.join(current_folder, new_name)

            os.rename(full_path, new_full_path)
            print(f"Renamed: {filename} → {new_name}")

# Example usage:
add_prefix_to_current_folder_files("Adventure_")