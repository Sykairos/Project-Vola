import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

url = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/spotify.zip"
df = pd.read_csv(url)

# régler le problème du genre qui apparait 2 fois
df.genre = df.genre.str.replace('Children’s Music',"Children's Music")

# mettre key, time_signature, mode en colonne
df = pd.concat([df, df["key"].str.get_dummies()], axis=1)
df = pd.concat([df, df["time_signature"].str.get_dummies()], axis=1)
df = pd.concat([df, df["mode"].str.get_dummies()], axis=1)

# drop les 3 colonnes que l'on a get_dummies()
df.drop(["key", "mode", "time_signature"], axis=1, inplace=True)

# créer une df avec les genres en get_dummies()
df_genres = pd.concat([df, df["genre"].str.get_dummies()], axis=1)
# pour les genres
df_average = df_genres.copy()

df_genres.drop("genre", axis=1, inplace=True)

# scale les données 
scaler = MinMaxScaler().fit(df_genres[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']])
df_genres[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']] = scaler.transform(df_genres[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']])
   
df_average[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']] = MinMaxScaler().fit_transform(df_average[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']])

# pour les genres
df_average = df_average.drop("popularity", axis=1).groupby("genre", as_index=False).mean()
df_average["genre"] = df_average["genre"].apply(lambda x: x.lower())

df_genres2 = df_genres.copy() # SAR

# GroupBy (track_id) en vue de regrouper les tracks avec plusieurs genres
cols = list(df_genres2.columns)

# dico pour définir les fonctions d'aggrégation séparément par colonne
# mean() sur les paramètres numériques non genres, et sum() sur les get_dummies des genres

df_genres2.track_name = df_genres2.track_name.apply(lambda s: [s])
df_genres2.artist_name = df_genres2.artist_name.apply(lambda s: [s])

dico = {}
for k in range(2):
    dico[cols[k]] = 'sum'
for k in range(3, 32):
    dico[cols[k]] = 'mean'
for k in range(32, len(cols)):
    dico[cols[k]] = 'sum'

df_genres3 = df_genres2.copy().groupby('track_id', as_index=False).agg(dico)

df_genres3.track_name = df_genres3.track_name.apply(lambda l: l[0])
df_genres3.artist_name = df_genres3.artist_name.apply(lambda l: l[0])

# pour que ça ne soit pas case sensitive, on garde l'autre colonne pour afficher les données avec les bonnes
# maj/minuscule
df_genres3["track_name_low"] = df_genres3["track_name"].apply(lambda x : x.lower())
df_genres3["artist_name_low"] = df_genres3["artist_name"].apply(lambda x : x.lower())



df_chill = pd.read_csv(r'C:\Users\Administrateur\Desktop\Hackathon\CSV\chill.csv', sep=",")
df_party = pd.read_csv(r'C:\Users\Administrateur\Desktop\Hackathon\CSV\party.csv', sep=",")
df_sad = pd.read_csv(r'C:\Users\Administrateur\Desktop\Hackathon\CSV\sad.csv', sep=",")
df_sexy = pd.read_csv(r'C:\Users\Administrateur\Desktop\Hackathon\CSV\sexy.csv', sep=",")
df_sleepy_night = pd.read_csv(r'C:\Users\Administrateur\Desktop\Hackathon\CSV\sleepy_night.csv', sep=",")
df_sport = pd.read_csv(r'C:\Users\Administrateur\Desktop\Hackathon\CSV\sport.csv', sep=",")

def key(x):
    dico={0 : "C", 
          1 : "C#", 
          2 : "D", 
          3 : "D#", 
          4 : "E", 
          5 : "F", 
          6 : "F#", 
          7 : "G", 
          8 : "G#", 
          9 : "A", 
          10 : "A#", 
          11 : "B"}
    return dico[x]

def time_signature(x):
    dico={0 : "0/4", 1 : "1/4", 3 : "3/4",4 : "4/4",5 : "5/4"}
    return dico[x]

def reshaping(df_name):
    df_name["mode"] = df_name["mode"].apply(lambda x: "Major" if x == 0 else "Minor")
    df_name["key"] = df_name["key"].apply(key)
    df_name["time_signature"] = df_name["time_signature"].apply(time_signature)
    df_name = pd.concat([df_name, df_name["key"].str.get_dummies()], axis=1)
    df_name = pd.concat([df_name, df_name["time_signature"].str.get_dummies()], axis=1)
    df_name = pd.concat([df_name, df_name["mode"].str.get_dummies()], axis=1)
    df_name.drop(["key", "mode", "time_signature"], axis=1, inplace=True)
    return df_name

def transform_df(df):
    new_df = pd.DataFrame(df.mean())
    return new_df.T

df_sexy = reshaping(df_sexy)
df_sleepy_night = reshaping(df_sleepy_night)
df_sport = reshaping(df_sport)
df_chill = reshaping(df_chill)
df_party = reshaping(df_party)
df_sad = reshaping(df_sad)


df_chill['0/4']=0
df_chill['1/4']=0
df_chill = df_chill[['Unnamed: 0', 'genre', 'artist_name', 'track_name', 'track_id',
       'popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
       'valence', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G',
       'G#', '0/4', '1/4', '3/4', '4/4', '5/4', 'Major', 'Minor']].copy()
       
df_party['0/4']=0
df_party['1/4']=0
df_party['3/4']=0
df_party['5/4']=0
df_party = df_party[['Unnamed: 0', 'genre', 'artist_name', 'track_name', 'track_id',
       'popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
       'valence', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G',
       'G#', '0/4', '1/4', '3/4', '4/4', '5/4', 'Major', 'Minor']].copy()
       
df_sad['0/4'] = 0
df_sad['1/4'] = 0
df_sad = df_sad[['Unnamed: 0', 'genre', 'artist_name', 'track_name', 'track_id',
       'popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
       'valence', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G',
       'G#', '0/4', '1/4', '3/4', '4/4', '5/4', 'Major', 'Minor']].copy()

df_sexy["0/4"] = 0
df_sexy["1/4"] = 0
df_sexy = df_sexy[['Unnamed: 0', 'genre', 'artist_name', 'track_name', 'track_id',
       'popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
       'valence', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G',
       'G#','0/4','1/4', '3/4', '4/4', '5/4', 'Major', 'Minor']].copy()


df_sleepy_night["0/4"] = 0
df_sleepy_night["1/4"] = 0
df_sleepy_night["5/4"] = 0
df_sleepy_night = df_sleepy_night[['Unnamed: 0', 'genre', 'artist_name', 'track_name', 'track_id',
       'popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
       'valence', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G',
       'G#','0/4', '1/4', '3/4', '4/4', '5/4', 'Major', 'Minor']].copy()


df_sport["0/4"] = 0
df_sport["1/4"] = 0
df_sport["3/4"] = 0
df_sport["5/4"] = 0
df_sport = df_sport[['Unnamed: 0', 'genre', 'artist_name', 'track_name', 'track_id',
       'popularity', 'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
       'valence', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G',
       'G#','0/4', '1/4', '3/4', '4/4', '5/4', 'Major', 'Minor']].copy()

df_sexy = transform_df(df_sexy)
df_sleepy_night = transform_df(df_sleepy_night)
df_sport = transform_df(df_sport)
df_chill = transform_df(df_chill)
df_party = transform_df(df_party)
df_sad = transform_df(df_sad)

list_df = (df_chill, df_party, df_sad, df_sexy, df_sleepy_night, df_sport)
list_genre = ("chill", "party","sad", "sexy", "sleepy_night", "sport")

for item in list_df :
    item[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']] = scaler.transform(item[['acousticness',
       'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
       'loudness', 'speechiness', 'tempo', 'valence']])

df_chill["ambiance"] = "chill"
df_party["ambiance"] = "party"
df_sad["ambiance"] = "sad"
df_sexy["ambiance"] = "sexy"
df_sleepy_night["ambiance"] = "sleepy_night"
df_sport["ambiance"] = "sport"

df_ambiance = pd.concat(list(list_df), ignore_index=True)




df_genres3.to_csv(r'C:\Users\Administrateur\Desktop\Hackathon\Final\df_genres3.csv', sep=",")
df_average.to_csv(r'C:\Users\Administrateur\Desktop\Hackathon\Final\df_average.csv', sep=",")
df_ambiance.to_csv(r'C:\Users\Administrateur\Desktop\Hackathon\Final\df_ambiance.csv', sep=",")
