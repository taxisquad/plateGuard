

# TODO add ability to put metadata to front of frame showing time-data, also add file namin convention
def save_encypt(nonce, tag, ciphertext, frame_num, car_num, path):

    file_name = str(frame_num) + "_" + str(car_num)
    file_out = open(path + file_name + ".wfc", "wb")
    [file_out.write(x) for x in (nonce, tag, ciphertext)]


def save_frame(buf, out):

    for b in buf.frames:
        out.write(b)


