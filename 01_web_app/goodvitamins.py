# Web app packages
import streamlit as st
import boto3
import joblib

# Data science packages
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from random import shuffle


# Sidebar panel
st.sidebar.markdown(
    '''
    # GoodVitamins
    *quickly distills the top representative reviews of iHerb's bestselling Vitamin Supplement product.*
    
    ---
    '''
)
product = st.sidebar.selectbox(
    'Select a vitamin product:', ('',
        'Vitamin D3 + K2, Soy-Free, 125 mcg (5000 IU), 60 VegCaps',
        'Vitamins D and K with Sea-Iodine, 125 mcg (5,000 IU), 60 Capsules',
        'Vegan Vitamin D3 & K2, 62.5 mcg (2,500 IU), 60 Vegan Capsules',
        'Liquid Vitamin D-3, Extra Strength, 25 mcg (1,000 IU), 1 fl oz (30 ml)',
        "ADAM, Superior Men's Multi, 90 Softgels",
        'Vitamin Code, RAW prenatal, 180 Vegetarian Capsules',
        'One Daily, Maximum, 100 Tablets',
        'Immunity, Sodium Ascorbate, Crystalline Powder, 8 oz (227 g)',
        'Ester-C, 1,000 mg, 120 Vegetarian Coated Tablets',
        'Basic Nutrients 2/Day, 60 Capsules',
        'Vitamin A, 3,000 mcg (10,000 IU), 110 Softgels',
        "Animal Parade, Children's Chewable Multi-Vitamin and Mineral, Natural Assorted Flavors, 180 Animal-Shaped Tablets",
        'Big Friends, Chewable Vitamin C, Tangy Orange, 250 mg, 90 Chewable Tablets',
        'Zoo Friends with Extra C, Orange, 60 Chewable Tablets',
        'Lil Brainies, Omega Tri-Blend & DHA, Kids Multivitamin, Ages 2+, 60 Gummies',
        'Naturally Sourced Vitamin E, 67 mg (100 IU), 100 Softgels',
        'Folic Acid, 400 mcg, 250 Easy to Swallow Tablets',
        'B Complex Plus Vitamin C, 100 Tablets',
        'B-Complex #12, 60 Capsules',
        'B-50 Complex, Prolonged Release, 60 Tablets',
        'Stress B-Complex, 60 Capsules'
    )
)
k = st.sidebar.slider(
    'Select number of distinct reviews:',
    2, 4, value=2, step=1
)
n = st.sidebar.slider(
    'Select number of examples to show for similar review:',
    1, 3, value=2, step=1
)
stars = st.sidebar.slider(
    'Filter reviews by star rating:',
    1, 5, value=(1, 5), step=1
)
st.sidebar.markdown(
    '''
    ---
    Created by [Andy Pham](https://www.linkedin.com/in/andyphamto/)
    '''
)


file_dict = {
        'High Potency Vitamin D-3, 5,000 IU, 240 Softgels' : '56_High_Potency_Vitamin_D_3_5_000_IU_240_Softgels_',
        'Vitamin D3 + K2, Soy-Free, 125 mcg (5000 IU), 60 VegCaps' : "111_Vitamin_D3_K2_Soy_Free_125_mcg_5000_IU_60_VegCaps_",
        'Vitamins D and K with Sea-Iodine, 125 mcg (5,000 IU), 60 Capsules' : "132_Vitamins_D_and_K_with_Sea_Iodine_125_mcg_5_000_IU_60_Capsules_",
        'Vegan Vitamin D3 & K2, 62.5 mcg (2,500 IU), 60 Vegan Capsules' : "90_Vegan_Vitamin_D3_K2_62_5_mcg_2_500_IU_60_Vegan_Capsules_",
        'Liquid Vitamin D-3, Extra Strength, 25 mcg (1,000 IU), 1 fl oz (30 ml)' : "67_Liquid_Vitamin_D_3_Extra_Strength_25_mcg_1_000_IU_1_fl_oz_30_ml_",
        "ADAM, Superior Men's Multi, 90 Softgels" : "1_ADAM_Superior_Men_s_Multi_90_Softgels_",
        'Vitamin Code, RAW prenatal, 180 Vegetarian Capsules' : "100_Vitamin_Code_RAW_prenatal_180_Vegetarian_Capsules_",
        'One Daily, Maximum, 100 Tablets' : "75_One_Daily_Maximum_100_Tablets_",
        'Immunity, Sodium Ascorbate, Crystalline Powder, 8 oz (227 g)' : "62_Immunity_Sodium_Ascorbate_Crystalline_Powder_8_oz_227_g_",
        'Ester-C, 1,000 mg, 120 Vegetarian Coated Tablets' : "41_Ester_C_1_000_mg_120_Vegetarian_Coated_Tablets_",
        'Basic Nutrients 2/Day, 60 Capsules' : "20_Basic_Nutrients_2_Day_60_Capsules_",
        'Vitamin A, 3,000 mcg (10,000 IU), 110 Softgels' : "92_Vitamin_A_3_000_mcg_10_000_IU_110_Softgels_",
        "Animal Parade, Children's Chewable Multi-Vitamin and Mineral, Natural Assorted Flavors, 180 Animal-Shaped Tablets" : "12_Animal_Parade_Children_s_Chewable_Multi_Vitamin_and_Mineral_Natural_Assorted_Flavors_180_Animal_Shaped_Tablets_",
        'Big Friends, Chewable Vitamin C, Tangy Orange, 250 mg, 90 Chewable Tablets' : "21_Big_Friends_Chewable_Vitamin_C_Tangy_Orange_250_mg_90_Chewable_Tablets_",
        'Zoo Friends with Extra C, Orange, 60 Chewable Tablets' : "133_Zoo_Friends_with_Extra_C_Orange_60_Chewable_Tablets_",
        'Lil Brainies, Omega Tri-Blend & DHA, Kids Multivitamin, Ages 2+, 60 Gummies' : "64_Lil_Brainies_Omega_Tri_Blend_DHA_Kids_Multivitamin_Ages_2_60_Gummies_",
        'Naturally Sourced Vitamin E, 67 mg (100 IU), 100 Softgels' : "74_Naturally_Sourced_Vitamin_E_67_mg_100_IU_100_Softgels_",
        'Folic Acid, 400 mcg, 250 Easy to Swallow Tablets' : "45_Folic_Acid_400_mcg_250_Easy_to_Swallow_Tablets_",
        'B Complex Plus Vitamin C, 100 Tablets' : "13_B_Complex_Plus_Vitamin_C_100_Tablets_" ,
        'B-Complex #12, 60 Capsules' : "18_B_Complex_12_60_Capsules_",
        'B-50 Complex, Prolonged Release, 60 Tablets' : "14_B_50_Complex_Prolonged_Release_60_Tablets_",
        'Stress B-Complex, 60 Capsules' : "83_Stress_B_Complex_60_Capsules_"
    
    }


# Initialize S3 client for loading data
#s3_client = boto3.client('s3')

@st.cache
def load_reviews(csv_file, pkl_file):
    '''
    Load sentences & sentence vectors from goodvitamins S3 bucket
    '''
    # Download pickle file from S3
    #s3_client.download_file('andy-pham72', pkl_file, 'vectors.pkl')

    # Read in sentences CSV as dataframe & filter by selected star ratings
    df = pd.read_csv(f'{csv_file}')
    filter_index = df[(df['individual_rating'] >= stars[0]) & (df['individual_rating'] <= stars[1])].index
    df = df.loc[filter_index].reset_index(drop=True)
    sentences = df['review_contents'].copy()

    # Read in sentence vectors & filter similarly
    sentence_vectors = joblib.load(f'{pkl_file}')
    sentence_vectors = sentence_vectors[filter_index]

    return sentences, sentence_vectors


@st.cache
def find_opinions(sentence_vectors, k):
    '''
    Run a k-means model on sentence vectors & return cluster centres
    '''
    kmeans_model = KMeans(n_clusters=k)
    kmeans_model.fit(sentence_vectors)
    cluster_centres = kmeans_model.cluster_centers_
    return cluster_centres


@st.cache
def get_opinions(sentences, sentence_vectors, cluster_centres, k):
    '''
    Find the 3 closest sentences to each cluster centre
    '''
    # Initialize dataframe to store cluster centre sentences
    df = pd.DataFrame()
    
    # Set the number of cluster centre points to look at when calculating uniformity score
    centre_points = int(len(sentences) * 0.01)
    
    # Loop through number of clusters selected
    for i in range(k):

        # Define cluster centre
        centre = cluster_centres[i]

        # Calculate inner product of cluster centre and sentence vectors
        ips = np.inner(centre, sentence_vectors)

        # Find the 3 sentences with the highest inner products
        top_indices = pd.Series(ips).nlargest(3).index
        top_sentences = list(sentences[top_indices])

        # Randomly shuffle top sentences (for variety)
        # shuffle(top_sentences)        16
        
        # Calculate uniformity score for cluster
        centre_ips = pd.Series(ips).nlargest(centre_points)
        uniformity_score = np.mean(centre_ips)
        
        # Create new row with cluster's top 10 sentences and uniformity score
        new_row = pd.Series([top_sentences, uniformity_score])
        
        # Append new row to master dataframe
        df = df.append(new_row, ignore_index=True)
        
    # Rename dataframe columns
    df.columns = ['sentences', 'Uniformity']

    # Sort dataframe by uniformity score, from highest to lowest
    df = df.sort_values(by='Uniformity', ascending=False).reset_index(drop=True)

    return df


if product != '':
    '''
    # What are users saying about:
    ###
    '''

    product_id = file_dict[product].split('_')[0]
    st.image(f'/product_images/{product_id}.jpg')

    '---'

    # Create S3 file names
    csv_file = f'/model_output/{file_dict[product]}.csv'
    pkl_file = f'/model_output/{file_dict[product]}.pkl'

    # Load sentences & sentence vectors
    sentences, sentence_vectors = load_reviews(csv_file, pkl_file)

    # Find cluster centres
    cluster_centres = find_opinions(sentence_vectors, k)

    # Find the three closest sentences to each cluster centre
    sentences_df = get_opinions(sentences, sentence_vectors, cluster_centres, k)

    uni_scores = dict()

    # Loop through number of clusters selected
    for i in range(k):
        
        # Save uniformity score & sentence list to variables
        uni_score = round(sentences_df.loc[i]['Uniformity'], 3)
        uni_scores.update({f'Opinion #{i+1}':uni_score})
        sents = sentences_df.loc[i]['sentences'].copy()
        
        f'**Opinions #{i+1}**'

        # Print out number of sentences selected
        for j in range(n):
            f'- {sents[j]}'

        '---'
    
    '''
    ### Output analysis: Opinion uniformity scores
    '''
    uniformity_df = pd.DataFrame()
    uniformity_df = uniformity_df.append(uni_scores, ignore_index=True)
    uniformity_df.index = ['']
    st.table(uniformity_df)
    '''
    *Each opinion's uniformity score reflects the amount of semantic uniformity across that opinion's most central sentences. Generally speaking, the higher an opinion's uniformity score, the more confident we can be that its sentences represent a widespread opinion within the full set of reviews.*
    
    *Scores range between 0 and 1, though any value above 0.4 should be considered high. Uniformity scores will change as the number of opinions is adjusted. Opinions are automatically displayed in descending order of their uniformity scores.* 
    '''


if product == '':
    '''

    # :pill: GoodVitamins

    *Applies NLP and Unsupervised Machine Learning techniques to find the most common reviews of bestselling vitamin supplements.*

    ### :bulb: How to do

    Select a product from the menu on the left. The GoodVitamins algorithm will go through the list of reviews then display the most representative reviews to you.

    There are some options that allow you to adjust as the numbers of distinct review, or filter the reviews by the star rating.

    *(There will be some null values when you adjust the star from 1 to 3 because some products do not have low star reviews)*

    ### :pill: The Vitamin Products
    '''
    
    st.image("/product_images/List_of_products.png", use_column_width = True)

    '''
 
    ### :thought_balloon: The Review Data

    All the reviews were scraped by my self-made [iHerb webscraper](https://github.com/Andy-Pham-72/GoodVitamins/tree/main/iHerb%20webscraper)   


    ### :computer: How The Algorithm Works

    Using Universal Sentence Encoder, K-means Clustering, Inner Product Calculation. Please check the code, exploration, and data analysis on my [Github](https://github.com/Andy-Pham-72/GoodVitamins).


    ### :mega: Special Thanks

    GoodVitamins project was created as part of my capstone project for my Data Science Diploma at [BrainStation](https://brainstation.io).

    The framework of GoodVitamins were inspired by the project [BetterReads](https://github.com/williecostello/BetterReads) by [Willie Costello](https://www.linkedin.com/in/williecostello/). It's such a big help for me to finish my capstone project.

    I would like to thank my educators: [Adam Thorsteinson](https://www.linkedin.com/in/adam-thorsteinson-670a0552/), [Govind Suresh](https://www.linkedin.com/in/govindsuresh/), [Luan Nguyen](https://www.linkedin.com/in/lnguyen7-nd/), and [Ben Polzin](https://www.linkedin.com/in/bpolzin/). Last but not least, many thanks to my amazing classmates.
    
    '''



