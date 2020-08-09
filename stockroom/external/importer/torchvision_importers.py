try:
    from torchvision import datasets
except ModuleNotFoundError:
    pass
import numpy as np

from stockroom.external.importer.base import BaseImporter


class TorchvisionCommon(BaseImporter):

    def __init__(self, dataset, train):
        self.dataset = dataset
        self.split = 'train' if train else 'test'
        self.sample_img, self.sample_label = self._process_data(*self.dataset[0])

    def column_names(self):
        return f'{self.name}-{self.split}-image', f'{self.name}-{self.split}-label'

    def shapes(self):
        return self.sample_img.shape, self.sample_label.shape

    def dtypes(self):
        return self.sample_img.dtype, self.sample_label.dtype

    @staticmethod
    def _process_data(img, lbl):
        # TODO: memory copy
        img = np.ascontiguousarray(np.transpose(np.array(img), (2, 0, 1)))
        img = img.astype(np.float32) / 255
        lbl = np.array(lbl)
        return img, lbl

    def __iter__(self):
        for img, label in self.dataset:
            yield self._process_data(img, label)

    def variability_status(self):
        return False

    def __len__(self):
        return len(self.dataset)

    @classmethod
    def gen_splits(cls, dataset, root):
        dataset_splits = []
        dataset_splits.append(dataset(root=root, train=True, download=True))
        dataset_splits.append(dataset(root=root, train=False, download=True))
        return dataset_splits


class Cifar10(TorchvisionCommon):
    name = 'cifar10'

    @classmethod
    def gen_splits(cls, root):
        dataset = datasets.CIFAR10
        dataset_splits = super().gen_splits(dataset, root)
        return dataset_splits


class Mnist(TorchvisionCommon):
    name = 'mnist'

    @classmethod
    def gen_splits(cls, root):
        dataset = datasets.MNIST
        dataset_splits = super().gen_splits(dataset, root)
        return dataset_splits


class FashionMnist(TorchvisionCommon):
    name = 'fashion_mnist'

    @classmethod
    def gen_splits(cls, root):
        dataset = datasets.FashionMNIST
        dataset_splits = super().gen_splits(dataset, root)
        return dataset_splits


class ImageFolder(BaseImporter):
    name = 'imagefolder'

    def __init__(self, root):
        self.dataset = datasets.ImageFolder(root)


        self.sample_img, self.sample_label = self._hangar_transform(*self.dataset[0])

    def column_names(self):
        return