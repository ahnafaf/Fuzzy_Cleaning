
import pandas as pd

words = [
  ["car", "automobile", "vehicle", "acr", "cr"],
  ["dog", "canine", "pooch", "dgo", "dogg"],
  ["book", "novel", "publication", "bok", "boook"],
  ["computer", "pc", "laptop", "comuter", "latop"],
  ["city", "town", "metropolis", "ctiy", "citi"],
  ["pen", "marker", "writing instrument", "pn", "pek"],
  ["tree", "oak", "pine", "trew", "tere"],
  ["cat", "feline", "kitty", "ct", "kat"],
  ["bicycle", "bike", "cycle", "bicycel", "byke"],
  ["house", "home", "dwelling", "huse", "hme"],
  ["phone", "mobile", "cellular", "pone", "phne"],
  ["shirt", "blouse", "top", "shit", "shrt"],
  ["chair", "seat", "furniture", "cair", "cheir"],
  ["shoe", "footwear", "sneaker", "soe", "shu"],
  ["plant", "flora", "vegetation", "plnt", "pant"],
  ["cup", "mug", "beverage container", "cp", "cupp"],
  ["watch", "timepiece", "wristwatch", "wath", "wtch"]
]

words = pd.DataFrame(words, columns=["Word", "Synonym1", "Synonym2", "Typo1", "Typo2"])

typos = words[["Typo1", "Typo2"]]

typos.to_csv('typos.csv', index=False)