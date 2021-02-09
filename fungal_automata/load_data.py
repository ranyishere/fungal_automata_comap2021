import pandas as pd


# Phellinus gilvus -> p.gilv
# Xylobolus subpileatus -> x.sub
# Porodisculus pendulus -> p.pend
# Merulius tremellosus ->  m.trem
# Tyromyces chioneus -> t.chion

data = pd.read_csv('pnas.1712211114.sd01.csv')

print("data: ", data.head())
