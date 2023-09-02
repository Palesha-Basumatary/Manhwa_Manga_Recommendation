import re
from math import sqrt
import urllib.request
from urllib.error import HTTPError
import cv2
import numpy as np
import pandas as pd
import streamlit as st

manhwa_df = pd.read_csv('data\Manhwa_data.csv')

#Building the Recommendation Model
manhwa_df['id'] = manhwa_df.index

#separating the genre/tags from brackets and '' to make a list of tags
manhwa_df.tags= manhwa_df.tags.map(lambda x:x.replace('\'','').replace('[','').replace(']','')).tolist()
manhwa_df['tags']=manhwa_df['tags'].str.split(', ')


tag_df = manhwa_df.copy()
## we take the accounts of genres present in the manga and assign 1 to those genres
for index, row in manhwa_df.iterrows():
    for tag in row['tags']:
        tag_df.at[index,tag] = 1

tag_df=tag_df.fillna(0)


def recommend(inputmanhwa):
    title = list(inputmanhwa['title'].unique())
    
    inputId = manhwa_df[manhwa_df['title'].isin(title)]
    
    my_manhwa = inputId.drop(columns=['tags','year','cover'])
    my_manhwa=my_manhwa.reset_index(drop=True)
    
    my_genre = tag_df[tag_df['id'].isin(my_manhwa['id'].tolist())]
    my_genre=my_genre.reset_index(drop=True)
    
    mygenretable = my_genre.drop(columns=['title','description','rating','year','tags','cover','id'])
    
    myprofile = mygenretable.transpose()
    myprofile = myprofile.dot(my_manhwa['rating'])
    
    genreTable = tag_df.set_index(tag_df['id'])
    x= genreTable[~genreTable.isin(inputId)]
    genreTable=x.dropna()
    genreTable = genreTable.drop(columns=['id','description','title','tags','year','cover'])
    
    recommendationTable_df = ((genreTable*myprofile).sum(axis=1))/(myprofile.sum())
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
    #values_to_remove = list(my_manhwa.values)
    #recom=recommendationTable_df[~recommendationTable_df.isin(values_to_remove)]
    final_recom=manhwa_df.loc[manhwa_df['id'].isin(recommendationTable_df.head(20).keys())]
    for i in final_recom.index:
        st.write(final_recom['title'][i])
        st.write(final_recom['description'][i])
#       url = final_recom['cover'][i]
#        if url:
#            try:
#                #Open the URL and read the image
#                response = urllib.request.urlopen(url)
#                img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
#                image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#
#                #Display the image
#                st.image(image, channels="BGR", use_column_width=True, caption="Image")
#            except HTTPError as http_err:
#                st.error(f"HTTP Error: {http_err.code}")
#            except Exception as e:
#                st.error(f"Error: {str(e)}")
       
    



st.write("""
# Manhwa Recommendation App

This app recommends Manhwas/Mangas acoording to the user input!

""")

#taking user input
with st.form("user_input"):
    st.write(" User's Any 5 Manga/Manhwa Reviews")
    m1 = st.selectbox('Manhwa Name 1:-',manhwa_df['title'],key='m1')
    r1 = st.slider('Rating',0.0,5.0,0.0,step=0.1,format="%f",key='r1')
    
    m2 = st.selectbox('Manhwa Name 2:-',manhwa_df['title'],key='m2')
    r2 = st.slider('Rating',0.0,5.0,0.0,step=0.1,format="%f",key='r2')
    
    m3 = st.selectbox('Manhwa Name 3:-',manhwa_df['title'],key='m3')
    r3 = st.slider('Rating',0.0,5.0,0.0,step=0.1,format="%f",key='r3')
    
    m4 = st.selectbox('Manhwa Name 4:-',manhwa_df['title'],key='m4')
    r4 = st.slider('Rating',0.0,5.0,0.0,step=0.1,format="%f",key='r4')

    m5= st.selectbox('Manhwa Name 5:-',manhwa_df['title'],key='m5')
    r5 = st.slider('Rating',0.0,5.0,0.0,step=0.1,format="%f",key='r5')

    data = [{'title':m1,'rating':r1},
            {'title':m2,'rating':r2},
            {'title':m3,'rating':r3},
            {'title':m4,'rating':r4},
            {'title':m5,'rating':r5}
    ]
    inputdf=pd.DataFrame(data)
    submitted=st.form_submit_button('Submit',)
    if submitted:
        recommend(inputdf)



