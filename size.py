def getsize(toponym):
    delta = str(max(float(str(abs(float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[0]) -
                                  float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[0])))[0:6]),
                    float(str(abs(float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[1]) -
                                  float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[1])))[0:6])))

    for i in range(len(delta)):
        if delta[i] != '0' and delta[i] != '.':
            delta = list(delta)
            delta[i] = '1'
            delta = str(''.join(delta))
            delta = delta[0:i + 1]
            break

    return delta