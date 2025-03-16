from math import pow

# various functions to deal with data sent over the protocol
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
    if type(array) == tuple:
        array = list(array)

    return str(array).replace(" ", "").strip("[]")

# quantizing msg to at least 16 bytes (-_-)
# this really hurts my soul but if it works,
def msg_quantize(string):

    for i in range(4, 7):
        s = int(pow(2, i))

        if s == len(string) + 1:
            return string
        elif s > len(string) + 1:
            fill = s - 1 - len(string)

            for j in range(fill):
                string += "\r"

            return string
    
    return None