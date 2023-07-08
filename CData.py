import pandas as pd
import re
from spellchecker import SpellChecker


#Fixing typos


class DF(pd.DataFrame):

    def reduce_repeats(self):

        pattern = re.compile(r"(.)\1{2,}")

        def apply_reduction(word):
            return pattern.sub(r"\1\1", str(word))

        return self.applymap(apply_reduction)
    
    

    def spell_check(self):
        
        spell = SpellChecker()
        
        for col in self.columns:
            
            new_col = col+"_new"
            col_pos = self.columns.get_loc(col)
            corrected = []
            
            for misspelled in self[col]:
                corrected.append(spell.correction(str(misspelled))) 
            self.insert(col_pos +1, new_col, corrected)
            corrected = []
        
        return self
        
            

        
typos = pd.read_csv("typos.csv")
typos.columns = typos.columns.str.lower()


removed = DF(typos).reduce_repeats()

checked = DF(removed).spell_check()






