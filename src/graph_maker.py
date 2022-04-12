import plotly.express as px
import pandas as pd
import config

def make_graphs():
    print("starting graphs")
    df = pd.read_csv("toronto_all_data.csv")
    df.set_index("Year", inplace=True)
    print(df.loc["Snowy Owl"])

    for i, row in df.iterrows():
        print(row)
        fig = px.line(row, y=row.name, title="Test")
        fig.write_html(config.data_dir + "\\toronto\\graphs\\" + row.name + "_test.html")

    df.to_html("toronto_data.html")


make_graphs()
