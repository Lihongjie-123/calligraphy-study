import os
import pandas as pd

grade_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "var",
            "grade")
grade_file_path = os.path.join(grade_dir, "三.csv")

data = pd.read_csv(open(grade_file_path))
df = \
    data.sort_values(
        by=['practise_count', 'use_time'],
        ascending=[False, True]
    )
df.to_csv(grade_file_path, index=False)
