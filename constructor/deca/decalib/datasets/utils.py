import logging
import os

import numpy as np
import torch

logger = logging.getLogger(__name__)

###############################################################################
## CONSTANTS

TRAIN_DATA_SIZE = (400, 400)
TEST_DATA_SIZE = (608, 608)

###############################################################################
## UTILTY FUNCTION

def shape(tensor):
    r"""Utility function to return the shape of tensors of various types."""
    if tensor is None:
        return None
    if isinstance(tensor, (list, tuple)):
        return tuple(shape(t) for t in tensor)
    if isinstance(tensor, (torch.Tensor, torch.autograd.Variable)):
        return list(tensor.size())
    elif isinstance(tensor, np.ndarray):
        return list(tensor.shape)

    return len(tensor)


def default_optimizer(params):
    r"""Returns the default optimizer if one is not provided when setting up
    a training session.

    See :py:class:`train.Trainer`.
    """
    return torch.optim.Adam(params, lr=1e-5)


def check_mkdir(path, increment=False):
    r"""Only creates a directory if it does not exist already.  Emits an
    warning if it exists. When 'increment' is true, it creates a directory
    nonetheless by incrementing an integer at its end.
    """
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        logger.warning('The given path already exists (%s)', path)
        if increment:
            trailing_int = 0
            while os.path.isdir(path):
                basename = os.path.basename(path)
                split = basename.split('_')
                if split[-1].isdigit():
                    basename = '_'.join(split[:-1])
                path = os.path.join(
                        os.path.dirname(path),
                        basename + '_{}'.format(trailing_int))
                trailing_int += 1
            os.makedirs(path)
            logger.info('Created the directory (%s) instead', path)

    return path


def fast_hist(y_pred, y, num_classes=2):
    r"""Generic function for computing a confusion matrix of matching
    predictions. It is taken from [1].

    NOTE: The ground truths correspond to the rows of the returned confusion
    matrix, while the predictions to its columns!

    [1]:
    https://github.com/zijundeng/pytorch-semantic-segmentation/
    """
    mask = (y >= 0) & (y < num_classes)
    hist = np.bincount(
            num_classes * y[mask] + y_pred[mask],
            minlength=(num_classes**2)).reshape(num_classes, num_classes)

    return hist


def evaluate(y_preds=None, ys=None, num_classes=2, hist=None, eps=1e-10):
    r"""Generic function for computing various prediction metrics. It is taken
    from [1].

    [1]:
    https://github.com/zijundeng/pytorch-semantic-segmentation/
    """
    # compute confusion matrix if not provided
    if hist is None:
        hist = np.zeros((num_classes, num_classes))
        for lp, lt in zip(y_preds, ys):
            hist += fast_hist(lp.flatten(), lt.flatten(), num_classes)

    # axis 0: gt, axis 1: prediction
    acc = np.diag(hist).sum() / (hist.sum() + eps)
    acc_cls = np.diag(hist) / (hist.sum(axis=1) + eps)
    acc_cls = np.nanmean(acc_cls)
    iu = np.diag(hist) / \
            (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist) + eps)
    mean_iu = np.nanmean(iu)
    freq = hist.sum(axis=1) / (hist.sum() + eps)
    fwavacc = (freq[freq > 0] * iu[freq > 0]).sum()

    # put them together
    common_metrics = (acc, acc_cls, mean_iu, fwavacc)

    # return them if we have more than 2 classes
    if num_classes > 2:
        return common_metrics

    # if we have exactly two classes, also compute precision/recall/f1
    # NOTE: The following assumes the histogram is built using the above
    # `fast_hist` function. Check out its doc on the expected semantics.
    true_pos = hist[1, 1]
    false_pos = hist[0, 1]
    false_neg = hist[1, 0]
    precision = true_pos / (true_pos + false_pos + eps)
    recall = true_pos / (true_pos + false_neg + eps)
    f1_score = 2. * ((precision * recall) / (precision + recall + eps))

    return common_metrics + (precision, recall, f1_score)


def torch_shuffle(*arrays):
    r"""Shuffles mutlple tensors by the first dimension."""
    indices = np.random.permutation(shape(arrays[0])[0])

    return tuple(None if a is None else a[indices] for a in arrays)


def train_val_split(*arrays, val_size, shuffle=False):
    r"""Splits a dataset which contains multiple instances on the first
    dimension into trainin/validation datasets, using a validation percentage.
    """
    # shuffle data
    if shuffle:
        arrays = torch_shuffle(*arrays)
    n_val = int(val_size * shape(arrays[0])[0])

    return tuple((a[n_val:], a[:n_val]) for a in arrays)
