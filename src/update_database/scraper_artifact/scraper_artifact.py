import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class ScrapeNewLinkArtifact:
    new_links : np.array

@dataclass
class ScrapeDataArtifact:
    dataframe : pd.DataFrame
