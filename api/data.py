import dataset

db = dataset.connect("sqlite:///data.db")
beams = db['beams']

def insertBeam(beam):
    beams.insert(beam)

def readBeams():
    result = beams.all()
    print(result)
    return result