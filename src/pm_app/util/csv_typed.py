# converts python arrays to ProtocolStackV2 compatible csv-typed arrays and vice versa

def convert_from(csv):
    out = list()

    for s in csv.split(","):
        try:
            out.append(int(s))
        except ValueError:
            continue

    return out

def convert_to(array):
    return str(array).replace(" ", "").strip("[]")