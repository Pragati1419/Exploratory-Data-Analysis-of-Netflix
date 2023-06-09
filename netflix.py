""" Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
 """
import pandas as pd 
import matplotlib.pyplot as plt

netflix = pd.read_csv('/content/netflix_titles.csv')
netflix

netflix.info()

netflix.describe()

missing_data = netflix.isna().sum().sort_values(ascending=False)
missing_data

netflix_isna = pd.isna(netflix['director'])
netflix[netflix_isna]

netflix['show_id'].duplicated().any()

netflix['date_added']= pd.to_datetime(netflix['date_added'].str.strip(), format= "%B %d, %Y") 
netflix

type_data = netflix.type.unique()
type_data

"""# Exploratory Data Analysis"""

# year with the most added movies/tv-shows
netflix_release_year = netflix.date_added.dt.year.astype('Int64').value_counts()
netflix_release_year

#The month with the most added movies/tv-shows
netflix_release_month = netflix.date_added.dt.month.astype('Int64').value_counts()
netflix_release_month

#Day with the most added movies/tv-shows
netflix_release_day = netflix.date_added.dt.day.astype('Int64').value_counts()
netflix_release_day

#Number of Movies vs. TV-Shows
netflix_type = netflix.type.value_counts()
netflix_type

#About the Movies/TV-Shows
#The year with the most releases movies/tv-shows
movietv_release_year = netflix.release_year.value_counts()
movietv_release_year

#The oldest movie/tv-show on streaming
netflix[netflix['release_year']== 1925]

#Top 30 Cast members with the most content
#New dataset for the cast count
cast_count = netflix.copy()
cast_count = pd.concat([cast_count, netflix['cast'].str.split(",", expand=True)], axis=1)
cast_count = cast_count.melt(id_vars=["type","title"], value_vars=range(44), value_name="Cast_name")
cast_count = cast_count[cast_count["Cast_name"].notna()]
cast_count["Cast_name"] = cast_count["Cast_name"].str.strip()
cast_count

cast_count.Cast_name.value_counts()[:30]

"""# Visualization"""

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

#Movies vs. TV-Shows
px.histogram(netflix, x= 'type', color= 'type',
             title="Movies vs. TV-Shows",
             color_discrete_sequence= px.colors.sequential.Sunsetdark)

#Number of Movies/TV-Shows added by Year
px.histogram(netflix, x= netflix['date_added'].dt.year, color= netflix['type'],
             title="Netflix number of Movie/TV Show by year",
             color_discrete_sequence= px.colors.sequential.Sunsetdark,  
              labels=dict(x="Year", color= "Type")                     
                   )

"""Number of Movies/TV-Shows added by Month

Dropping 'NA' records from the column 'date_added'
Dropping 10 records from the column 'date_added' that contain 'NA' values
"""

#counting the number of 'NA' on the column 'date_added'
netflix['date_added'].isna().sum()

#dropping 'NA'
netflix = netflix.dropna(subset=['date_added'])
px.histogram(netflix, x= netflix['date_added'].dt.month, color= netflix['type'],
             color_discrete_sequence= px.colors.sequential.Sunsetdark,
             title="Movies/TV Shows added by Month",
             labels=dict(x="Month"))

#Number of Movies/TV-Shows added by Day
px.histogram(netflix, x= netflix['date_added'].dt.day,color= netflix['type'],
             color_discrete_sequence= px.colors.sequential.Sunsetdark,            
             title="Movies/TV Shows added by Day",
             labels=dict(x="Day"))

px.histogram(netflix, x= 'release_year', color= 'type',
             title="Number of Movies/TV-Shows by year of release",
             color_discrete_sequence= px.colors.sequential.Sunsetdark,  
             labels={'release_year':'Year of release'}                     
                   )

px.histogram(cast_count, x= 'Cast_name', color= 'type',
    title="Top 30 Cast members with the most streaming content",
    color_discrete_sequence= px.colors.sequential.Sunsetdark).update_xaxes(
    categoryorder="total descending",range=(0, 30))
