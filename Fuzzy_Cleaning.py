import os
import pandas as pd
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


data = pd.read_csv(r"https://raw.githubusercontent.com/MSajidur-Rahman/Fuzzy_Cleaning/main/Test_Data/Task1%20Data/Categories.csv")
data = data.drop(columns="Unnamed: 1").squeeze()


def meta_labelling(series: pd.Series, n: int):
    """
    Sorts a pandas series into meta categories based on semantics using GPT-3.5 model.
    
    Parameters
    ----------
    series (pd.Series): The input series to be sorted. 
    n (int): The number of meta categories to create.
        
    Returns
    ------- 
    (pd.DataFrame): A DataFrame with the meta categories as columns and the sorted items as values.
    """
    
    llm = ChatOpenAI(model_name = "gpt-3.5-turbo",
                 temperature=0.3)
    
    template = ChatPromptTemplate.from_messages([
    ("system", """You will be provided a list and will sort them into {number} meta categories based on semantics.
                    Return each category in one line. The format should be similar to the following:
                    Meta Label1: Item1, Item2, Item3
                    Meta Label2: Item1, Item2, Item3"""),     
    ("human", "{data}")])
     
    formatted_template = template.format_messages(number = str(n), data = str(series.tolist()))

    response = llm(formatted_template).content

    return response_to_df(response)


def response_to_df(response):
    """
    Convert a response string into a DataFrame of meta categories and sorted items.
    
    Parameters
    ----------
    response (str): The response string to be converted.
        
    Returns
    ------- 
    (pd.DataFrame): A DataFrame containing meta categories as columns and sorted items as values.
    """
    
    df_dict = {}
    for line in response.split("\n"):
        line = line.split(":")
        key = line[0]
        values = [val.strip() for val in line[1].split(",")]
        df_dict[key] = values

    df = pd.DataFrame.from_dict(df_dict, orient='index').T
    return df


openai.api_key = os.getenv("OPENAI_API_KEY")

output = meta_labelling(data, 8)
