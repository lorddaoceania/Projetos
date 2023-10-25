import gzip
import os

def gzip_folder(folder_path, output_file):
    with gzip.open(output_file, 'wb') as gz_file:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                with open(file_path, 'rb') as file:
                    gz_file.write(file.read())

folder_to_compress = input('Enter the folder path: ')

output_gzip_file = 'compressed.gz'

gzip_folder(folder_to_compress, output_gzip_file)

print('Done')