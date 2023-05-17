import streamlit as st
import pandas as pd
import itertools
import holoviews as hv
from holoviews import opts, dim, Dataset
from bokeh.models import CustomJS, DatePicker

def main():
    path = 'data/without_content.tsv.xz'
    df = pd.read_csv(path, sep='\t', compression='xz')
    df['countries'] = df['countries'].apply(eval)
    df['date'] = pd.to_datetime(df['date'])

    hv.extension('bokeh')

    st.title('Chord-Diagramm')

    selected_date = st.date_input("Wähle Datum",
                                  value=pd.to_datetime('2022-01-01'),
                                  min_value=pd.to_datetime('2022-01-01'),
                                  max_value=pd.to_datetime('2022-12-31'))

    filtered_data = df[df['date'] == pd.to_datetime(selected_date)]['countries'].tolist()
    threshold = 10
    edges_list = []
    for connection in filtered_data:
        for pair in itertools.combinations(connection, 2):
            edges_list.append(pair)
    edges_df = pd.DataFrame(edges_list, columns=['source', 'target'])
    edges_count = edges_df.groupby('source').count()
    edges_count.columns = ['count']
    filtered_countries = edges_count[edges_count['count'] >= threshold].index
    filtered_edges_df = edges_df[edges_df['source'].isin(filtered_countries) & edges_df['target'].isin(filtered_countries)]
    edges_ds = Dataset(filtered_edges_df, ['source', 'target'])
    chord = hv.Chord(edges_ds).select(value=(1, None))
    chord.opts(
        opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(),
                   labels='index', node_color=dim('index').str(), width=600, height=600)
    )
    st.bokeh_chart(hv.render(chord, backend='bokeh'))

if __name__ == "__main__":
    main()
