import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def get_data():
    url='https://drive.switch.ch/index.php/s/cxW0xrmQXdGL1VJ/download'
    return pd.read_csv(url)

df = get_data()

st.title(body='CO2-Emissions')
st.header('CO2-Emissions per region in most recent year')

df_last = df[df['year']==max(df['year'])]

co2_per_region = df_last.groupby('region')['co2'].sum()
co2_per_region.sort_values(inplace=True, ascending=True)

st.subheader('Text Elements and Column Layout')
st.markdown("[text elements](https://docs.streamlit.io/library/api-reference/text)")

st.markdown("[layouts](https://docs.streamlit.io/library/api-reference/layout)")
left_column, right_column = st.columns(2)
with left_column:
    st.subheader('Subheader left column')
    st.text('text element in left column')
with right_column:
    st.subheader('Subheader right column')
    st.text('text element in right column')

    
st.subheader('Various charting libraries are supported')
st.markdown("[chart elements](https://docs.streamlit.io/library/api-reference/charts)")
st.text('this is a matplotlib-chart:')
fig, ax = plt.subplots()
ax.spines[:].set_visible(False)
ax.spines['top'].set_visible(True)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top') 

ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

ax.barh(co2_per_region.index, co2_per_region.values)

st.pyplot(fig)

st.subheader('DataFrame display')
st.markdown("[data elements](https://docs.streamlit.io/library/api-reference/data)")
st.text('Click and Ctrl-F to search the table!')
st.dataframe(data=df, use_container_width=True)

