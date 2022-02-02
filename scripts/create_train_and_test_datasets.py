import os
import torch
import torchvision


def save_images(dataset, classes, output_dir):
    for i, (img, label) in enumerate(dataset):
        dn = os.path.join(os.getcwd(), output_dir, classes[label])
        try:
            os.makedirs(dn)
        except FileExistsError:
            pass
        fn = f"{i}.png"
        torchvision.utils.save_image(img, os.path.join(dn, fn))


def create_train_and_test_datasets():
    params = {
        "seed": 1234,
        "input_dir": "../data/dataset",
        "output_dir_train": "data/dataset_train",
        "output_dir_test": "data/dataset_test",
        "resize_size": 256,
        "train_test_ratio": 0.8,
    }
    data_dir = os.path.join(os.getcwd(), params["input_dir"])
    transform = torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize(params["resize_size"]),
            torchvision.transforms.ToTensor(),
        ]
    )
    dataset = torchvision.datasets.ImageFolder(data_dir, transform=transform)
    n_train = int(params["train_test_ratio"] * len(dataset))
    n_test = len(dataset) - n_train
    dataset_train, dataset_test = torch.utils.data.random_split(
        dataset,
        [n_train, n_test],
        generator=torch.Generator().manual_seed(params["seed"]),
    )
    assert len(dataset_train) + len(dataset_test) == len(dataset)
    save_images(dataset_train, dataset.classes, params["output_dir_train"])
    save_images(dataset_test, dataset.classes, params["output_dir_test"])


create_train_and_test_datasets()
