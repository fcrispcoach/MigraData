from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()

def generate_old_data():
    data = [{
        "id": fake.uuid4(),
        "nome": fake.name(),
        "valor": np.random.randint(50, 150)
    } for _ in range(100)]
    return pd.DataFrame(data)

def generate_new_data():
    df = generate_old_data()
    df = df.sample(n=105, replace=True).reset_index(drop=True)
    df["valor"] = df["valor"] + np.random.randint(-10, 10, size=len(df))
    return df


generate_old_data().to_csv("/home/pyshell/Dev/MigraData/old_data.csv", index=False)
generate_new_data().to_csv("/home/pyshell/Dev/MigraData/new_data.csv", index=False)