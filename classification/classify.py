import joblib
import pandas as pd

import sys, os
sys.path.append('../')
from utils import VFH


def predict_class(pcd):
    df = pd.DataFrame()

    desc = VFH(pcd)
    df.loc[0, [i for i in range(len(desc))]] = desc

    mean, covariance = pcd.compute_mean_and_covariance()

    size = pcd.get_max_bound() - pcd.get_min_bound()
    center = pcd.get_center()

    df.at[0, [308, 309, 310]] = mean
    df.at[0, [311, 312, 313]] = covariance[0]
    df.at[0, [314, 315, 316]] = covariance[1]
    df.at[0, [317, 318, 319]] = covariance[2]
    df.at[0, [320, 321, 322]] = size
    df.at[0, [323, 324, 325]] = center

    svm = joblib.load('svm.pkl')
    proba = svm.predict_proba([dfgit .loc[0].values])

    return dict(zip(['human', 'other', 'wear'], proba[0]))

