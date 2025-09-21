import dataset

db = dataset.connect("sqlite:///data.db")
beams = db['beams']

def insertBeam(beam):
    tags.insert(beam)

def readBeams():
    return beams.all()