import mutagen, os, time, concurrent.futures
from mutagen import flac

def coverRead (width: int, height: int):
    """
    Function responsible for reading the picture file that includes the cover art. If there is
    not such file, it returns blank variable.
    """
    coverArt = mutagen.flac.Picture()
    try:
        if (os.path.isfile("cover.jpg")):
            with open("cover.jpg","rb") as f:
                coverArt.data = f.read()
            coverArt.mime = u"image/jpeg"
        elif (os.path.isfile("cover.png")):
            with open("cover.png","rb") as f:
                coverArt.data = f.read()
            coverArt.mime = u"image/png"
        else:
            raise FileNotFoundError
        
        coverArt.type = mutagen.id3.PictureType.COVER_FRONT
        coverArt.depth = 16
        coverArt.width = width
        coverArt.height = height
    except FileNotFoundError:
        print("Couldn't load cover-art.")
    finally:
        return coverArt


def appendTag (discindex: int = 1, discnum: int = 1):
    """
    Function responsible for appending ID tags to all music files found in the directory.
    """
    with os.scandir() as it:
        for index, entry in enumerate(it,1):
            if not entry.name.startswith(".") and (entry.name.endswith(".flac") or entry.name.endswith(".mp3")) and entry.is_file():
                audioFile = mutagen.File(entry.name)
                title = entry.name[2:entry.name.rfind(".flac")].strip()
                if (title[0] == "-"):
                    title = title[1:].strip()
                audioFile["tracknumber"] = str(index)
                audioFile["title"] = title
                audioFile["artist"] = ARTIST
                audioFile["album"] = ALBUM
                audioFile["date"] = YEAR
                audioFile["genre"] = GENRE
                audioFile["discnumber"] = f"{discindex}/{discnum}"
                audioFile.add_picture(coverArt)
                audioFile.save()
 
if __name__ == "__main__":
    currentDirName = os.getcwd()
    ARTIST = currentDirName[currentDirName.rfind("\\")+1:currentDirName.find("-")].strip()
    ALBUM = currentDirName[currentDirName.find("-")+1:].strip()
    YEAR = input("Enter release date: ")
    GENRE = input("Enter genre: ")
    coverArt = coverRead(500,500)
    isFile = False
    t1 = time.perf_counter()

    with os.scandir() as it:
        for entry in it:
            if entry.is_file() and not (entry.name.endswith(".jpg") or entry.name.endswith(".png")):
                isFile = True
                break
    if isFile:
        appendTag()
    else:
        discs = len(os.listdir())
        for i in range (1,discs):
            os.chdir(f"CD{i}")
            appendTag(i,discs-1)
            os.chdir("..")
    t2 = time.perf_counter()
    print(round(t2 - t1, 2))