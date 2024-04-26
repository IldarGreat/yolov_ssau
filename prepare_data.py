import os
import random
import shutil
import requests
import zipfile

ZIP_FILE_NAME = 'file.zip'
EXTRACTED_ZIP_FILE_NAME = 'file'


def download_data():
    url = "https://storage.ai.ssau.ru/s/5qkEdcarYWRPmEc/download"
    print("Начинаю скачивать файл")
    response = requests.get(url)

    if response.status_code == 200:
        with open(ZIP_FILE_NAME, "wb") as file:
            file.write(response.content)
        print("Файл успешно скачан.")
        with zipfile.ZipFile(ZIP_FILE_NAME, 'r') as zip_ref:
            zip_ref.extractall(EXTRACTED_ZIP_FILE_NAME)
            print("Файл разархивирован")
    else:
        print("Ошибка при скачивании файла.")
    pass


def create_images_and_labels_folders():
    os.makedirs("images", exist_ok=True)
    os.makedirs("labels", exist_ok=True)

    for folder_name in range(1, 41):
        image_folder = f"{EXTRACTED_ZIP_FILE_NAME}/Summer_4200/{folder_name}"
        label_folder = f"{EXTRACTED_ZIP_FILE_NAME}/Summer_4200/{folder_name}/{folder_name}"

        for root, dirs, files in os.walk(image_folder):
            for image_file in files:
                if image_file.endswith('.JPG'):
                    shutil.copy(os.path.join(root, image_file), "images")

        for root, dirs, files in os.walk(label_folder):
            for label_file in files:
                if label_file.endswith('.txt'):
                    shutil.copy(os.path.join(root, label_file), "labels")
    pass


def split_data():
    os.makedirs("train/images", exist_ok=True)
    os.makedirs("train/labels", exist_ok=True)
    os.makedirs("test/images", exist_ok=True)
    os.makedirs("test/labels", exist_ok=True)
    os.makedirs("val/images", exist_ok=True)
    os.makedirs("val/labels", exist_ok=True)

    image_folder = "images"
    label_folder = "labels"

    image_files = os.listdir(image_folder)
    label_files = os.listdir(label_folder)

    random.shuffle(image_files)

    train_size = int(0.7 * len(image_files))
    test_size = int(0.2 * len(image_files))
    val_size = len(image_files) - train_size - test_size

    train_images = image_files[:train_size]
    test_images = image_files[train_size:train_size + test_size]
    val_images = image_files[train_size + test_size:]

    for image_file in train_images:
        shutil.copy(os.path.join(image_folder, image_file), "train/images")
    for image_file in test_images:
        shutil.copy(os.path.join(image_folder, image_file), "test/images")
    for image_file in val_images:
        shutil.copy(os.path.join(image_folder, image_file), "val/images")

    for image_file in train_images:
        label_file = os.path.splitext(image_file)[0] + ".txt"
        shutil.copy(os.path.join(label_folder, label_file), "train/labels")
    for image_file in test_images:
        label_file = os.path.splitext(image_file)[0] + ".txt"
        shutil.copy(os.path.join(label_folder, label_file), "test/labels")
    for image_file in val_images:
        label_file = os.path.splitext(image_file)[0] + ".txt"
        shutil.copy(os.path.join(label_folder, label_file), "val/labels")


pass

if __name__ == '__main__':
    download_data()
    create_images_and_labels_folders()
    split_data()

    shutil.rmtree(EXTRACTED_ZIP_FILE_NAME)
    os.remove(ZIP_FILE_NAME)

