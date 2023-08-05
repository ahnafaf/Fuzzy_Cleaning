import pandas as pd
import openai
import os

# Task 1: Meta Labelling

data = pd.read_csv(r"https://raw.githubusercontent.com/MSajidur-Rahman/Fuzzy_Cleaning/main/Test_Data/Task1%20Data/Categories.csv")
data = data.drop(columns = "Unnamed: 1").squeeze()

openai.api_key = os.getenv("OPENAI_API_KEY")

def Meta_Labelling(series,n):
    
    """
    Sorts a series into meta categories based on semantics.
    
    Args:
    series (pd.Series): The input series to be sorted.
    n (int): The number of meta categories to create.
    
    Returns:
    pd.DataFrame: A dataframe with the meta categories as columns and the sorted items as values.
    """
    
    system_message = f"""You will be provided a list and will sort them into {n} meta categories based on semantics.
                    Return each category in one line. The format should be similar to the following:
                    Meta Label1: Item1, Item2, Item3
                    Meta Label2: Item1, Item2, Item3"""
                    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.4,
    messages=[
    {"role": "system", "content": f"{system_message}"},
    {"role": "user", "content": f"{str(series.to_list())}"} 
    ])
    
    response = completion.choices[0]["message"]["content"]
    
    #converting the string response to a dataframe
    df_dict = {}
    for line in response.split("\n"):
        line = line.split(":")
        key = line[0]
        values = [val.strip() for val in line[1].split(",")]
        df_dict[key] = values
        
    df = pd.DataFrame.from_dict(df_dict, orient='index').T
    
    return df

output = (Meta_Labelling(data, 8))

