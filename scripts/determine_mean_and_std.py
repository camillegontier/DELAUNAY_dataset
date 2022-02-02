import os
import torch
import torchvision


def determine_mean_and_std():
    params = {
        "input_dir_train": "data/dataset_train",
    }

    data_dir_train = os.path.join(os.getcwd(), params["input_dir_train"])
    transform = torchvision.transforms.Compose(
        [torchvision.transforms.RandomCrop(112), torchvision.transforms.ToTensor(),]
    )
    dataset_train = torchvision.datasets.ImageFolder(
        data_dir_train, transform=transform
    )
    mean = torch.zeros(3)
    std = torch.zeros(3)
    n = 0
    for sample, label in dataset_train:
        mean += sample.mean(dim=(1, 2))
        std += sample.std(dim=(1, 2))
        n += 1
    mean /= n
    std /= n
    print(f"mean: {mean}, std: {std}")


determine_mean_and_std()
