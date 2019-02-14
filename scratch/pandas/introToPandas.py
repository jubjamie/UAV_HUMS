import numpy as np
import pandas as pd

dates = pd.date_range('20190204', periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

print(df)