import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###


@st.cache
def load_data():
    # Move this code into `load_data` function {{
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Cancer", "Sex"],
        var_name="Age",
        value_name="Deaths",
    )

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
    )

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

# }}
    return df


# Uncomment the next line when finished
df = load_data()


### P1.2 ###


st.write("## testing code 3 Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
year = st.slider(label="Year", min_value=df["Year"].min(), max_value=df["Year"].max())
subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
# replace with st.radio
sex = st.radio(label = "Sex", options = ["M", "F"], index = 1)
subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = st.multiselect(label = "Countries", options=df["Country"].unique(), default=["Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand"])
subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
cancer = st.selectbox(label = "Cancer", options = df["Cancer"].unique())
subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country"),
    color=alt.Color("Rate").scale(type="log", domain=(.00001,100000), clamp=True),
    tooltip=["Rate"]
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")



# Load the dataset from the URL
url = 'https://gist.githubusercontent.com/wangqianwen0418/3de32c2d4ce8dafb8d22e8264c03d781/raw/f2d5a4553a28ab3623ac8fd6806ad7fb7f752ac6/cancer_usa.csv'
df = pd.read_csv(url)

# Filter the dataset for children under 5 years old
df_under_5 = df[['Cancer', 'Sex', 'Age <5']].groupby(['Cancer'], as_index=False).sum()

# Sort the data by the number of deaths in children under 5 and get the top 10 causes
top_cancers_under_5 = df_under_5.sort_values(by='Age <5', ascending=False).head(10)

# Create a bar chart of the leading causes of cancer death in children under 5
bar_chart = alt.Chart(top_cancers_under_5).mark_bar().encode(
    x=alt.X('Age <5:Q', title='Number of Deaths'),
    y=alt.Y('Cancer:N', sort='-x', title='Cancer Type'),
    color='Cancer:N',
    tooltip=['Cancer', 'Age <5']
).properties(
    title='Top 10 Leading Causes of Cancer Deaths in Children Under 5',
    width=600,
    height=400
)

bar_chart