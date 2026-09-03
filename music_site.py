# ============================================================
# MUSIC SPACE
# これ1ファイルだけで動くFlask音楽サイト
# ============================================================

import sys
import subprocess
import os
import json
import uuid
import threading
import webbrowser
from datetime import datetime


# ============================================================
# Flaskがなければ自動インストール
# ============================================================

try:
    from flask import (
        Flask,
        request,
        redirect,
        url_for,
        send_from_directory,
        jsonify,
        render_template_string
    )

except ImportError:

    print("Flaskを自動インストールしています...")

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "flask"
        ]
    )

    from flask import (
        Flask,
        request,
        redirect,
        url_for,
        send_from_directory,
        jsonify,
        render_template_string
    )


# ============================================================
# Flask
# ============================================================

app = Flask(__name__)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MUSIC_FOLDER = os.path.join(
    BASE_DIR,
    "music"
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "music_data.json"
)

ACCESS_FILE = os.path.join(
    BASE_DIR,
    "access_counter.txt"
)


os.makedirs(
    MUSIC_FOLDER,
    exist_ok=True
)


# 最大100MB
app.config["MAX_CONTENT_LENGTH"] = (
    100 * 1024 * 1024
)


# ============================================================
# 曲データ
# ============================================================

def load_songs():

    if not os.path.exists(DATA_FILE):
        return []

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, list):
                return data

    except:
        pass

    return []


def save_songs(songs):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            songs,
            f,
            ensure_ascii=False,
            indent=2
        )


# ============================================================
# アクセスカウンター
# ============================================================

def add_access():

    count = 0

    if os.path.exists(ACCESS_FILE):

        try:

            with open(
                ACCESS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                count = int(
                    f.read().strip()
                )

        except:
            count = 0


    count += 1


    with open(
        ACCESS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            str(count)
        )


    return count


# ============================================================
# HTML・CSS・JavaScript
# ============================================================

HTML = """
<!DOCTYPE html>

<html lang="ja">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width,initial-scale=1.0"
>

<title>MUSIC SPACE</title>


<style>

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    min-height: 100vh;

    font-family:
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;

    color: #f4f7ff;

    background:

    radial-gradient(
        circle at 10% 0%,
        rgba(0,180,255,.17),
        transparent 34%
    ),

    radial-gradient(
        circle at 90% 10%,
        rgba(120,70,255,.15),
        transparent 35%
    ),

    linear-gradient(
        180deg,
        #040610,
        #080b17,
        #03050a
    );

    background-attachment: fixed;
}


.container {

    width: min(
        960px,
        94%
    );

    margin: auto;
}


/* ==============================
   HEADER
============================== */

header {

    text-align: center;

    padding:
        55px
        15px
        30px;
}


.logo {

    margin: 0;

    font-size:
        clamp(
            35px,
            8vw,
            65px
        );

    font-weight: 900;

    letter-spacing: .14em;

    background:

        linear-gradient(
            90deg,
            white,
            #56e5ff,
            #9881ff,
            white
        );

    -webkit-background-clip: text;

    background-clip: text;

    color: transparent;

    text-shadow:
        0
        0
        40px
        rgba(
            80,
            210,
            255,
            .15
        );
}


.subtitle {

    margin-top: 10px;

    font-size: 12px;

    letter-spacing: .25em;

    color: #8995b1;
}


.access {

    display: inline-block;

    margin-top: 18px;

    padding:
        8px
        16px;

    border-radius: 30px;

    color: #a7b7d5;

    background:
        rgba(
            255,
            255,
            255,
            .035
        );

    border:
        1px solid
        rgba(
            100,
            200,
            255,
            .15
        );

    font-size: 13px;
}


/* ==============================
   BOX
============================== */

.box {

    margin-bottom: 25px;

    padding: 24px;

    border-radius: 22px;

    background:
        rgba(
            10,
            15,
            30,
            .78
        );

    border:
        1px solid
        rgba(
            130,
            190,
            255,
            .12
        );

    box-shadow:
        0
        25px
        70px
        rgba(
            0,
            0,
            0,
            .3
        );
}


.box-title {

    margin:
        0
        0
        20px;

    font-size: 17px;

    letter-spacing: .1em;
}


/* ==============================
   UPLOAD
============================== */

.upload {

    display: grid;

    grid-template-columns:
        1fr
        1fr
        auto;

    gap: 12px;
}


input {

    min-height: 52px;

    width: 100%;

    padding: 12px;

    border-radius: 12px;

    border:
        1px solid
        rgba(
            255,
            255,
            255,
            .1
        );

    color: white;

    background: #080d1b;

    outline: none;
}


input:focus {

    border-color:
        #55dfff;
}


button,
.btn {

    min-height: 48px;

    border: 0;

    border-radius: 12px;

    padding:
        0
        20px;

    cursor: pointer;

    font-weight: 800;

    text-decoration: none;

    display: inline-flex;

    align-items: center;

    justify-content: center;

    transition: .2s;
}


button:hover,
.btn:hover {

    transform:
        translateY(-2px);
}


.upload-button {

    color: #041017;

    background:

        linear-gradient(
            135deg,
            #55e7ff,
            #9280ff
        );
}


/* ==============================
   RANKING
============================== */

.rank-row {

    display: flex;

    align-items: center;

    gap: 15px;

    padding:
        14px
        4px;

    border-bottom:
        1px solid
        rgba(
            255,
            255,
            255,
            .06
        );
}


.rank-row:last-child {

    border-bottom: none;
}


.rank-number {

    width: 45px;

    font-size: 20px;

    font-weight: 900;
}


.rank-name {

    flex: 1;

    font-weight: 700;
}


.rank-play {

    color: #7ce4ff;

    font-size: 13px;
}


/* ==============================
   MUSIC
============================== */

.song {

    padding: 22px;

    margin-bottom: 16px;

    border-radius: 18px;

    background:

        linear-gradient(
            145deg,
            rgba(
                255,
                255,
                255,
                .05
            ),
            rgba(
                255,
                255,
                255,
                .015
            )
        );

    border:
        1px solid
        rgba(
            255,
            255,
            255,
            .08
        );
}


.song-header {

    display: flex;

    align-items: center;

    justify-content:
        space-between;

    gap: 10px;
}


.song-name {

    margin: 0;

    font-size:
        clamp(
            21px,
            5vw,
            29px
        );

    font-weight: 800;
}


.play-count {

    color: #6fe5ff;

    white-space: nowrap;

    font-size: 13px;
}


audio {

    width: 100%;

    height: 55px;

    margin:
        18px
        0;
}


.actions {

    display: flex;

    gap: 10px;
}


.download {

    color: #dffaff;

    background:
        rgba(
            50,
            200,
            255,
            .10
        );

    border:
        1px solid
        rgba(
            50,
            200,
            255,
            .20
        );
}


.delete {

    color: #ffbdc8;

    background:
        rgba(
            255,
            70,
            100,
            .08
        );

    border:
        1px solid
        rgba(
            255,
            70,
            100,
            .18
        );
}


.empty {

    padding: 30px;

    text-align: center;

    color: #74819d;
}


footer {

    padding:
        15px
        0
        45px;

    text-align: center;

    color: #4c5870;

    font-size: 11px;

    letter-spacing: .2em;
}


/* ==============================
   スマホ
============================== */

@media(max-width:700px) {

    header {

        padding-top: 38px;
    }


    .box {

        padding: 17px;
    }


    .upload {

        grid-template-columns:
            1fr;
    }


    .song {

        padding: 17px;
    }


    .song-header {

        flex-direction: column;

        align-items:
            flex-start;
    }


    .actions {

        display: grid;

        grid-template-columns:
            1fr
            1fr;
    }


    .btn,
    .delete {

        width: 100%;
    }
}

</style>

</head>


<body>


<header>

<div class="container">

<h1 class="logo">
MUSIC SPACE
</h1>

<div class="subtitle">
SIMPLE MUSIC PLAYER
</div>

<div class="access">

ACCESS {{ access }}

</div>

</div>

</header>


<main class="container">


<!-- UPLOAD -->

<section class="box">

<h2 class="box-title">
UPLOAD MUSIC
</h2>


<form

class="upload"

action="/upload"

method="post"

enctype="multipart/form-data"

>


<input

type="text"

name="title"

placeholder="曲名"

required

>


<input

type="file"

name="music"

accept=".mp3,audio/mpeg"

required

>


<button

type="submit"

class="upload-button"

>

UPLOAD

</button>


</form>

</section>



<!-- RANKING -->

<section class="box">

<h2 class="box-title">

🏆 PLAY RANKING

</h2>


{% if ranking %}


{% for song in ranking[:10] %}


<div class="rank-row">


<div class="rank-number">


{% if loop.index == 1 %}

🥇

{% elif loop.index == 2 %}

🥈

{% elif loop.index == 3 %}

🥉

{% else %}

{{ loop.index }}

{% endif %}


</div>


<div class="rank-name">

{{ song.title }}

</div>


<div class="rank-play">

▶ {{ song.plays }} 回

</div>


</div>


{% endfor %}


{% else %}


<div class="empty">

まだランキングはありません

</div>


{% endif %}


</section>



<!-- MUSIC -->

<section class="box">

<h2 class="box-title">

MUSIC

</h2>


{% if songs %}


{% for song in songs %}


<div class="song">


<div class="song-header">


<h3 class="song-name">

{{ song.title }}

</h3>


<div

class="play-count"

id="count-{{ song.id }}"

>

▶ {{ song.plays }} 回

</div>


</div>



<audio

controls

preload="metadata"

data-song="{{ song.id }}"

>


<source

src="/music/{{ song.filename }}"

type="audio/mpeg"

>


</audio>



<div class="actions">


<a

class="btn download"

href="/download/{{ song.id }}"

>

DOWNLOAD

</a>



<form

action="/delete/{{ song.id }}"

method="post"

onsubmit="return confirm('この曲を削除しますか？');"

>


<button

type="submit"

class="delete"

>

DELETE

</button>


</form>


</div>


</div>


{% endfor %}


{% else %}


<div class="empty">

まだ曲がありません。

<br><br>

MP3をアップロードしてください。

</div>


{% endif %}


</section>


</main>


<footer>

MUSIC SPACE

</footer>



<script>

document
.querySelectorAll("audio")
.forEach(function(player) {


    let counted = false;


    player.addEventListener(
        "play",
        function() {


            if (counted) {
                return;
            }


            counted = true;


            const id =
                player.dataset.song;


            fetch(
                "/play/" + id,
                {
                    method: "POST"
                }
            )


            .then(function(response) {

                return response.json();

            })


            .then(function(data) {


                const element =
                    document.getElementById(
                        "count-" + id
                    );


                if (element) {

                    element.textContent =
                        "▶ "
                        + data.plays
                        + " 回";

                }


            });


        }
    );


    player.addEventListener(
        "ended",
        function() {

            counted = false;

        }
    );


});

</script>


</body>

</html>
"""


# ============================================================
# トップページ
# ============================================================

@app.route("/")
def home():

    access = add_access()

    songs = load_songs()


    songs_display = sorted(
        songs,
        key=lambda x:
            x.get(
                "created",
                ""
            ),
        reverse=True
    )


    ranking = sorted(
        songs,
        key=lambda x:
            x.get(
                "plays",
                0
            ),
        reverse=True
    )


    return render_template_string(
        HTML,
        songs=songs_display,
        ranking=ranking,
        access=access
    )


# ============================================================
# アップロード
# ============================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    title = request.form.get(
        "title",
        ""
    ).strip()


    file = request.files.get(
        "music"
    )


    if not title or not file:

        return redirect("/")


    if file.filename == "":

        return redirect("/")


    if "." not in file.filename:

        return "MP3を選んでください", 400


    extension = (
        file.filename
        .rsplit(".", 1)[1]
        .lower()
    )


    if extension != "mp3":

        return "MP3だけアップロードできます", 400


    filename = (
        uuid.uuid4().hex
        + ".mp3"
    )


    file.save(
        os.path.join(
            MUSIC_FOLDER,
            filename
        )
    )


    songs = load_songs()


    songs.append(
        {
            "id":
                uuid.uuid4().hex,

            "title":
                title,

            "filename":
                filename,

            "plays":
                0,

            "created":
                datetime.now().isoformat()
        }
    )


    save_songs(
        songs
    )


    return redirect("/")


# ============================================================
# 音楽ファイル
# ============================================================

@app.route(
    "/music/<filename>"
)
def music(filename):

    return send_from_directory(
        MUSIC_FOLDER,
        filename
    )


# ============================================================
# 再生回数
# ============================================================

@app.route(
    "/play/<song_id>",
    methods=["POST"]
)
def play(song_id):

    songs = load_songs()


    for song in songs:

        if song["id"] == song_id:

            song["plays"] = (
                song.get(
                    "plays",
                    0
                )
                + 1
            )


            save_songs(
                songs
            )


            return jsonify(
                plays=song["plays"]
            )


    return jsonify(
        plays=0
    )


# ============================================================
# ダウンロード
# ============================================================

@app.route(
    "/download/<song_id>"
)
def download(song_id):

    songs = load_songs()


    for song in songs:

        if song["id"] == song_id:

            return send_from_directory(

                MUSIC_FOLDER,

                song["filename"],

                as_attachment=True,

                download_name=
                    song["title"]
                    + ".mp3"
            )


    return "曲がありません", 404


# ============================================================
# 削除
# ============================================================

@app.route(
    "/delete/<song_id>",
    methods=["POST"]
)
def delete(song_id):

    songs = load_songs()

    new_songs = []


    for song in songs:

        if song["id"] == song_id:

            path = os.path.join(
                MUSIC_FOLDER,
                song["filename"]
            )


            if os.path.exists(path):

                try:

                    os.remove(path)

                except:
                    pass


        else:

            new_songs.append(
                song
            )


    save_songs(
        new_songs
    )


    return redirect("/")


# ============================================================
# 起動
# ============================================================

def open_browser():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


if __name__ == "__main__":

    print("")
    print("==========================")
    print(" MUSIC SPACE")
    print("==========================")
    print("")
    print("ブラウザを自動で開きます")
    print("")


    threading.Timer(
        1.5,
        open_browser
    ).start()


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )