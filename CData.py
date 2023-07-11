import pandas as pd
import re
from spellchecker import SpellChecker
from thefuzz import process
import os
import openai
import numpy as np
from sklearn.cluster import KMeans


class CD(pd.DataFrame):
    
    def new_cols(self, skip_first=None): #Used by other funcs
        
        null_cols = []
        for col in self.columns[1:] if skip_first else self.columns:
            null_cols.append(col + "checked")
            col_pos = self.columns.get_loc(col)
            self.insert(col_pos + 1, null_cols[-1], None)
                    
        return null_cols



    def implimentation(self, func,skip_first=None): #Used by other funcs
        
        null_cols = self.new_cols(skip_first)
        iter_nulls = iter(null_cols)
            
        for col in self.columns[1:] if skip_first else self.columns:
            if col not in null_cols:
                corrected = []
                
                for word in self[col]:
                    corrected.append(func(word))
                add_col = next(iter_nulls)
                self[add_col] = self[add_col].fillna(pd.Series(corrected))
            
        return self
            
    
    def reduce_repeats(self): #Replaces words in place

        pattern = re.compile(r"(.)\1{2,}")

        def apply_reduction(word):
            return pattern.sub(r"\1\1", str(word))

        return self.applymap(apply_reduction)


    def spell_check(self):
        spell = SpellChecker()
    
        def apply_correction(word):
            return spell.correction(word)
    
        return self.implimentation(apply_correction,skip_first=False)
    
    
    
    def fuzzed(self):
        
        def apply_correction(word):
            return process.extractOne(word, self.iloc[:,0])[0]
            
        return self.implimentation(apply_correction,skip_first=True)


    
    def embed(self, openai_api_key): #Used by other funcs
        openai.api_key = openai_api_key
        df_flat = self.values.flatten().tolist()
        embeds = (openai.Embedding.create(model="text-embedding-ada-002",input=df_flat))
        embeds = [ d['embedding'] for d in embeds['data']]
        embeds = embeds/np.linalg.norm(embeds,axis=1,keepdims=True)
        return embeds,df_flat
        
    def k_means(self, openai_api_key, n_clusters=8):
        embeds,df_flat = self.embed(openai_api_key)
        cluster_model = KMeans(n_clusters=n_clusters,n_init="auto").fit(embeds)
        array = cluster_model.labels_
        
        def formater(self,array): #Probably should be made into its own func to be used by other funcs
            pairs = {}
            for num, val in zip(array, df_flat):
                if num in pairs:
                    pairs[num].append(val)
                else:
                    pairs[num] = [val]
                    
            long = 0
            for num,vals in pairs.items():
                if len(vals) > len(pairs[long]):
                     long = num
            for num in pairs:
                if len(pairs[num]) < len(pairs[long]):
                    pairs[num] += [np.nan] * (len(pairs[long])-len(pairs[num]))
                    
            return pd.DataFrame(pairs)
        
        return formater(self, array)
    
#For Testing
def match(df): #Assumes first col contains valid values and last col contains checked values
    if df.iloc[:, -1].isin(df.iloc[:, 0]).all():
        return True
    else:
        lst = df[~df.iloc[:, -1].isin(df.iloc[:, 0])]
        return lst
        
df = pd.read_csv(r"countries,cars,food.csv")
openai_api_key = os.getenv("openai_api_key")

pairs = CD(df).k_means(openai_api_key,n_clusters=3)







