import pandas as pd
import re
from spellchecker import SpellChecker
from thefuzz import process


class base(pd.DataFrame):
    
    def new_cols(self,skip_first=None): #Issue: Adds cols after all cols, not just the ones with mistakes
        
        null_cols = []
        for col in self.columns[1:] if skip_first else self.columns:
            null_cols.append(col + "_new")
            col_pos = self.columns.get_loc(col)
            self.insert(col_pos + 1, null_cols[-1], None)
                    
        return null_cols



    def application(self,func,skip_first=None):
        
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
            

class CD(base):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        
      
    def reduce_repeats(self): #Replaces words in place

        pattern = re.compile(r"(.)\1{2,}")

        def apply_reduction(word):
            return pattern.sub(r"\1\1", str(word))

        return self.applymap(apply_reduction)



    def spell_check(self):
        spell = SpellChecker()
    
        def apply_correction(word):
            return spell.correction(word)
    
        return self.application(apply_correction,skip_first=False)
    
    
    
    def fuzzed(self):
        
        def apply_correction(word):
            return process.extractOne(word, self.iloc[:,0])[0]
            
        return self.application(apply_correction,skip_first=True)
        

countries = pd.read_csv("countries.csv")
typos = pd.read_csv("typos.csv")


removed = CD(typos).reduce_repeats()

typos_checked = CD(typos).spell_check()
countries_checked = CD(countries).spell_check()
fuzzings = CD(countries).fuzzed()

