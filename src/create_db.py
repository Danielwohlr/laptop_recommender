import os

import pandas as pd
import numpy as np
from scipy.spatial import distance

def create_db(
        num_laptops: int = 1000,
        filepath: str = './res/laptop_db.csv'
    ) -> None:
    """
    Parameters
    ----------

    Returns
    -------
    None
    """

    # Generate random data for each column
    data = {
        'id': [f'Laptop_{i+1}' for i in range(num_laptops)],
        'Expensive': np.random.randint(0, 101, num_laptops),
        'CPU usage': np.random.randint(0, 101, num_laptops),
        'GPU': np.random.randint(0, 101, num_laptops),
        'Storage space': np.random.randint(0, 101, num_laptops),
        'RAM usage': np.random.randint(0, 101, num_laptops),
        'Screen resolution': np.random.randint(0, 101, num_laptops),
        'Weight': np.random.randint(0, 101, num_laptops),
        'Battery Life': np.random.randint(0, 101, num_laptops),
        'Camera Quality': np.random.randint(0, 101, num_laptops),
        'Indestructibility': np.random.randint(0, 101, num_laptops)
    }
    # Normalize data so that each row has a mean of 50, excluding the column 'id'
    # Create the DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(filepath, index=False)