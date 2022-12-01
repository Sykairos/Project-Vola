import pandas as pd
from sklearn.neighbors import NearestNeighbors
from tkinter import *
from PIL import ImageTk, Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

os.environ["SPOTIPY_CLIENT_ID"] = "fb852be077544d1a947dc04f73e6a5bc"
os.environ["SPOTIPY_CLIENT_SECRET"] = "3451faa7498c490fb6c7a7028d4d66d0"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


df_genres3 = pd.read_csv('df_genres3.csv', index_col=0, sep=",")
df_average = pd.read_csv('df_average.csv', index_col=0, sep=",")
df_ambiance = pd.read_csv('df_ambiance.csv', index_col=0, sep=",")


def algo(entry):
    # crée le model
    y = entry.lower().strip()

    X = df_genres3.copy().drop(["track_id", "popularity", "track_name", "artist_name",
                                "track_name_low", "artist_name_low"], axis=1)
    columns = X.columns

    model = NearestNeighbors(n_neighbors=31).fit(X)
    try:
        #  on cherche par genre
        genre_param = df_average[df_average["genre"] == y][columns]
        song_name = []
        artist_name = []
        track_id = []
        for i in range(0, 20):
            artist_name.append(df_genres3.iloc[model.kneighbors(genre_param)[1][0][i]]["artist_name"])
            song_name.append(df_genres3.iloc[model.kneighbors(genre_param)[1][0][i]]["track_name"])
            track_id.append(df_genres3.iloc[model.kneighbors(genre_param)[1][0][i]]["track_id"])
        return artist_name, song_name, track_id
    except ValueError:
        # si ca ne marche pas, on cherche par nom d'artiste
        # si len < 0 : artiste pas dans notre database
        if len(df_genres3[df_genres3["artist_name_low"] == y].sort_values("popularity", ascending=False)[
                   ["artist_name", "track_name"]][:21]["track_name"]) > 0:
            song_name = []
            artist_name = []
            track_id = []
            for i in range(0, 21):
                artist_name.append(df_genres3[df_genres3["artist_name_low"] == y]["artist_name"].values[0])
                song_name.append(
                    df_genres3[df_genres3["artist_name_low"] == y].sort_values("popularity", ascending=False)
                    ["track_name"].values[i])
                track_id.append(
                    df_genres3[df_genres3["artist_name_low"] == y].sort_values("popularity", ascending=False)
                    ["track_id"].values[i])
            return artist_name, song_name, track_id

        else:
            try:
                # recherche par track name
                song = df_genres3[df_genres3["track_name_low"] == y][columns]
                song_name = []
                artist_name = []
                track_id = []
                for i in range(0, 21):
                    artist_name.append(df_genres3.iloc[model.kneighbors(song)[1][0][i]]["artist_name"])
                    song_name.append(df_genres3.iloc[model.kneighbors(song)[1][0][i]]["track_name"])
                    track_id.append(df_genres3.iloc[model.kneighbors(song)[1][0][i]]["track_id"])
                return artist_name, song_name, track_id
            except ValueError:
                return "Please try with something else, maybe it's not in our database yet!"


def ambiance(mood):
    y = mood.lower().strip()

    X_test = df_genres3.copy().drop(["track_id", "popularity", "track_name", "artist_name",
                                     "track_name_low", "artist_name_low", 'A Capella', 'Alternative',
                                     'Anime', 'Blues', "Children's Music", 'Classical', 'Comedy', 'Country',
                                     'Dance', 'Electronic', 'Folk', 'Hip-Hop', 'Indie', 'Jazz', 'Movie',
                                     'Opera', 'Pop', 'R&B', 'Rap', 'Reggae', 'Reggaeton', 'Rock', 'Ska', 'Soul',
                                     'Soundtrack', 'World'], axis=1)
    columns = X_test.columns
    ambiance_param = df_ambiance[df_ambiance["ambiance"] == y][columns]

    model_test = NearestNeighbors(n_neighbors=31).fit(X_test)

    artist_name = []
    song_name = []
    track_id = []
    for i in range(0, 20):
        artist_name.append(df_genres3.iloc[model_test.kneighbors(ambiance_param)[1][0][i]]["artist_name"])
        song_name.append(df_genres3.iloc[model_test.kneighbors(ambiance_param)[1][0][i]]["track_name"])
        track_id.append(df_genres3.iloc[model_test.kneighbors(ambiance_param)[1][0][i]]["track_id"])
    return artist_name, song_name, track_id





### INTERFACE GRAPHIQUE
WIDTH = 1260
HEIGHT = 700

#Creating a new window and configurations
window = Tk()
window.title("VOLA LAUNCHER")
window.minsize(width=WIDTH, height=HEIGHT)
window.maxsize(width=WIDTH, height=HEIGHT)

#Creating a canvas
canvas = Canvas(width=WIDTH, height=HEIGHT, highlightthickness=0)
basewidth = WIDTH
load = Image.open("BG.png")
wpercent = (basewidth/float(load.size[0]))
hsize = int((float(load.size[1])*float(wpercent)))
load = load.resize((basewidth, hsize), Image.ANTIALIAS)
bg_img = ImageTk.PhotoImage(load)
canvas.create_image(WIDTH/2, HEIGHT/2, image=bg_img)
canvas.place(x=0, y=0)

# #Creating a canvas
# WIDTH_artwork= 150
# HEIGHT_artwork= WIDTH_artwork
# canvas_artwork = Canvas(width=WIDTH_artwork, height=HEIGHT_artwork, highlightthickness=0)
# basewidth_artwork = WIDTH_artwork
# load_artwork = Image.open("VOLA_LOGO.png")
# wpercent_artwork = (basewidth_artwork/float(load_artwork.size[0]))
# hsize_artwork = int((float(load_artwork.size[1])*float(wpercent_artwork)))
# load_artwork = load_artwork.resize((basewidth_artwork, hsize_artwork), Image.ANTIALIAS)
# artwork_img = ImageTk.PhotoImage(load_artwork)
# canvas_artwork.create_image(WIDTH_artwork/2, HEIGHT_artwork/2, image=artwork_img)
# canvas_artwork.place(x=215.573, y=205.096)

#Entries
entry = Entry(width=25)
#Add some text to begin with
entry.insert(END, string="Artist | Track | Genre")
entry.place(x=576.638, y=183.451)
entry.focus()
# entry.bind('<Button-1>',)
# (lambda : entry.select_range(0,END))

# def cover(track_str):
#     return sp.track(track_str)["album"]["images"][1][["url"]]

#Buttons

liste_algo= []
liste_ambiance= []

compteur = 0

def action():
    global compteur
    global liste_algo
    global liste_ambiance
    if clicked.get() == "No mood":
         liste_algo = algo(entry.get())
    else:
         liste_ambiance = ambiance(clicked.get())
    compteur = 0
    if clicked.get() == "No mood":
        label_artiste.config(text=liste_algo[0][0])
        label_titre.config(text=liste_algo[1][0])
    else:
        label_artiste.config(text=liste_ambiance[0][0])
        label_titre.config(text=liste_ambiance[1][0])
        da_var = liste_ambiance[2][0]



def replay():
    global compteur
    compteur -=1
    if clicked.get() == "No mood":
        try:
            label_artiste.config(text=liste_algo[0][compteur])
            label_titre.config(text=liste_algo[1][compteur])
        except:
            compteur = 0
    else:
        try:
            label_artiste.config(text=liste_ambiance[0][compteur])
            label_titre.config(text=liste_ambiance[1][compteur])
        except:
            compteur = 0


def skip():
    global compteur
    compteur += 1
    if clicked.get() == "No mood":
        try:
            label_artiste.config(text=liste_algo[0][compteur])
            label_titre.config(text=liste_algo[1][compteur])
        except:
            compteur = 0
    else:
        try:
            label_artiste.config(text=liste_ambiance[0][compteur])
            label_titre.config(text=liste_ambiance[1][compteur])
        except:
            compteur = 0

#calls action() when pressed
basewidth2 = 23
load2 = Image.open("search.gif")
wpercent2 = (basewidth2/float(load2.size[0]))
hsize2 = int((float(load2.size[1])*float(wpercent2)))
load2 = load2.resize((basewidth2, hsize2), Image.ANTIALIAS)
btn_ico = ImageTk.PhotoImage(load2)
button = Button(image=btn_ico, command=action, highlightthickness=0)
button.place(x=1017.15, y=181.451)


#calls action() when pressed
basewidth3 = 40
load3 = Image.open("replay.gif")
wpercent3 = (basewidth3/float(load3.size[0]))
hsize3 = int((float(load3.size[1])*float(wpercent3)))
load3 = load3.resize((basewidth3, hsize3), Image.ANTIALIAS)
btn_ico3 = ImageTk.PhotoImage(load3)
button_replay = Button(image=btn_ico3,command=replay, highlightthickness=0, bd= 0, width=25, height=10)
button_replay.place(x=226.5, y=434)


#calls action() when pressed
basewidth4 = 40
load4 = Image.open("skip.gif")
wpercent4 = (basewidth4/float(load4.size[0]))
hsize4 = int((float(load4.size[1])*float(wpercent4)))
load4 = load4.resize((basewidth4, hsize4), Image.ANTIALIAS)
btn_ico4 = ImageTk.PhotoImage(load4)
button_skip = Button(image=btn_ico4, command=skip, highlightthickness=0, bd= 0, width=25, height=10)
button_skip.place(x=327.969, y=434)

#Labels
canvas_titre = Canvas(width=163.478, height=10)
label_titre = Label(canvas_titre, text="Track Name", font="Open_Sans 10", anchor=CENTER)
canvas_titre.create_window(163.478/2, 6, window=label_titre, anchor=CENTER)
canvas_titre.place(x=207, y=522.449)

#Labels
canvas_artiste = Canvas(width=163.478, height=10)
label_artiste = Label(canvas_artiste, text="- Artist -", font="Open_Sans 10", anchor=CENTER)
canvas_artiste.create_window(163.478/2, 6, window=label_artiste, anchor=CENTER)
canvas_artiste.place(x=207, y=538)


# Drop List
drop_option = ["No mood", "Chill", "Party", "Sad", "Sexy", "Sleepy night", "Sport"]
clicked = StringVar()
clicked.set(drop_option[0])
droplist = OptionMenu(window, clicked, *drop_option)
droplist.config(width=15, bd=0, highlightthickness=0)
droplist.place(x=826, y=184.9)


window.mainloop()
