from scraper import search

if __name__ == "__main__":
    p = search("New York, NY")
    for y in range(len(p)):
        for x in range(len(p[0])):
            info = p[y][x]["hdpData"]["homeInfo"]
            print(info)
            if 'rentZestimate' not in info:
                print("Not in property")