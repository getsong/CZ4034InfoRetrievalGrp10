def formatJSON(inFileName, outFileName):
    # read input file, insert comma between JSON dicts
    with open(inFileName, 'r') as infile:
        content = infile.read()
        print(content)
        while content.find('}{') >= 0:
            content = content.replace('}{', '},{')

    # add opening and closing sign for JSON list
    content = '\n'.join(['[', content, ']'])

    # print for debugging
    print(content)

    # output to outFile specified
    with open(outFileName, 'w') as outfile:
        outfile.write(content)


if __name__ == '__main__':
    formatJSON('sports2.json', 'sportsFormatted2.json')
