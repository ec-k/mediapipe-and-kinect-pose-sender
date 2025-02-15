def unpack(landmarks):
    unpacked_landmakrs = []
    if landmarks.landmakrs is None:
        return unpacked_landmakrs
    for lm in landmarks.landmakrs:
        unpacked_landmakrs.append(lm)
    return unpacked_landmakrs
