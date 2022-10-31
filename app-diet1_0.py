import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn')

st.title('A Receipe Recommendation App ')
st.subheader('by Eric & Sirena')
df = pd.read_csv('All_Diets.csv')
df['percentage_protein'] =  100 * df['Protein(g)'] / (df['Protein(g)'] + df['Carbs(g)'] + df['Fat(g)'])
df['percentage_carbs'] = 100 * df['Carbs(g)'] / (df['Protein(g)'] + df['Carbs(g)'] + df['Fat(g)'])
df['percentage_fat'] = 100 * df['Fat(g)'] / (df['Protein(g)'] + df['Carbs(g)'] + df['Fat(g)'])
df_o = df

# add a ration to select eating habits
st.sidebar.subheader('Function 1: Analyze the receipes based on your likes')
diet_filter = st.sidebar.radio("Select You Diet type",('paleo', 'vegan', 'keto', 'mediterranean', 'dash','No specific diet'))

# add a multiselect by cuisine

cuisine_filter = st.sidebar.multiselect('Choose Your Preferred Cuisines', df.Cuisine_type.unique(), ('chinese','american','mediterranean'))

# add sliders to select the nutrigens in different receipes
st.sidebar.subheader('Function 2: Find the receipes based on the advice from your nutritionists of fitness instructur')
protein_filter = st.sidebar.slider('Percentage of protein', 0, 100, 100)
carbs_filter = st.sidebar.slider('Percentage of carbs', 0, 100, 100)
fat_filter = st.sidebar.slider('Percentage of fat', 0, 100, 100)

# Static analysis

st.subheader('Static Analysis')

fig, ax = plt.subplots(3,1,figsize=(15,15))

ax[0].boxplot([df[df.Diet_type == 'paleo'].percentage_protein,
                df[df.Diet_type == 'vegan'].percentage_protein,
                df[df.Diet_type == 'keto'].percentage_protein,
                df[df.Diet_type == 'mediterranean'].percentage_protein,
                df[df.Diet_type == 'dash'].percentage_protein],
                labels=['paleo', 'vegan', 'keto', 'mediterranean', 'dash'])
ax[1].boxplot([df[df.Diet_type == 'paleo'].percentage_carbs,
                df[df.Diet_type == 'vegan'].percentage_carbs,
                df[df.Diet_type == 'keto'].percentage_carbs,
                df[df.Diet_type == 'mediterranean'].percentage_carbs,
                df[df.Diet_type == 'dash'].percentage_carbs],
                labels=['paleo', 'vegan', 'keto', 'mediterranean', 'dash'])
ax[2].boxplot([df[df.Diet_type == 'paleo'].percentage_fat,
                df[df.Diet_type == 'vegan'].percentage_fat,
                df[df.Diet_type == 'keto'].percentage_fat,
                df[df.Diet_type == 'mediterranean'].percentage_fat,
                df[df.Diet_type == 'dash'].percentage_fat],
                labels=['paleo', 'vegan', 'keto', 'mediterranean', 'dash'])
ax[0].set_title('The percentage of protein in different diets') 
ax[1].set_title('The percentage of carbs in different diets')     
ax[2].set_title('The percentage of fat in different diets')                                  
st.pyplot(fig)



# filter by eating habits

if diet_filter == 'paleo':
    df = df[df.Diet_type == 'paleo']
elif diet_filter == 'vegan':
    df = df[df.Diet_type == 'vegan']
elif diet_filter == 'keto':
    df = df[df.Diet_type == 'keto']
elif diet_filter == 'mediterranean':
    df = df[df.Diet_type == 'mediterranean']
elif diet_filter == 'dash':
    df = df[df.Diet_type == 'dash']
elif diet_filter == 'No specific diet':
    df = df
# filter by cuisine

df = df[df.Cuisine_type.isin(cuisine_filter)]


# Function 1 anaylyze the choice
st.subheader('Function 1: Analyze the receipes based on your likes')
fig, ax =  plt.subplots(1,3, figsize=(20,8))
pic_protein = df.groupby('Cuisine_type').percentage_protein.mean()
pic_carbs = df.groupby('Cuisine_type').percentage_carbs.mean()
pic_fat = df.groupby('Cuisine_type').percentage_fat.mean()
pic_protein.plot.bar(ax=ax[0])
pic_carbs.plot.bar(ax=ax[1])
pic_fat.plot.bar(ax=ax[2])
ax[0].set_ylabel('Percentage of Protein')
ax[1].set_ylabel('Percentage of Carbs')
ax[2].set_ylabel('Percentage of Fat')
ax[0].set_xlabel('')
ax[1].set_xlabel('')
ax[2].set_xlabel('')
ax[0].set_title('The average percentage of proteins in the selected cuisines')
ax[1].set_title('The average percentage of carbs in the selected cuisines')
ax[2].set_title('The average percentage of fat in the selected cuisines')
st.pyplot(fig)

x = [df.percentage_protein.mean(),df.percentage_carbs.mean(),df.percentage_fat.mean()]
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
fig, ax = plt.subplots(figsize=(5,5))
ax.pie(x,labels = ['Protein','Carbs', 'Fat'], colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
ax.set_title('The occupation of protein, carbs and fat in your receipes')
st.pyplot(fig)
if df.percentage_protein.mean() >= df_o.percentage_protein.mean():
    st.write('Your favored receipes contains more protein than average.')
elif df.percentage_protein.mean() <= df_o.percentage_protein.mean():
    st.write('Your favored receipes contains less protein than average.')
if df.percentage_carbs.mean() >= df_o.percentage_carbs.mean():
    st.write('Your favored receipes contains more carbs than average.')
elif df.percentage_carbs.mean() <= df_o.percentage_carbs.mean():
    st.write('Your favored receipes contains less carbs than average.')
if df.percentage_fat.mean() >= df_o.percentage_fat.mean():
    st.write('Your favored receipes contains more fat than average.')
elif df.percentage_fat.mean() <= df_o.percentage_fat.mean():
    st.write('Your favored receipes contains less fat than average.')


# Function 2 find the recommended receipes
# filter by nutrigens

st.subheader('Function 2: Find the receipes based on the advice from your nutritionists of fitness instructur')
df = df[df.percentage_protein <= protein_filter]
df = df[df.percentage_carbs <= carbs_filter]
df = df[df.percentage_fat <= fat_filter]

st.write(df[['Recipe_name',	'Cuisine_type',	'Protein(g)', 'Carbs(g)', 'Fat(g)']])
