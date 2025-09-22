import dataset

db = dataset.connect("sqlite:///data.db")
beams = db['beams']

def insertBeam(beam):
    beams.insert(beam) # pyright: ignore[reportOptionalMemberAccess]

def readBeams():
    result = beams.all() # pyright: ignore[reportOptionalMemberAccess]
    print(result)
    return result