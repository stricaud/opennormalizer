def output_w(normalized_data):
    col = 0
    outbuf = ""
    while col < len(normalized_data):
        colbuf = normalized_data[col].replace("\"", "\\\"")
        outbuf += "\"" + colbuf + "\"" + ";"

        col += 1

    print(outbuf[:-1])

    return True