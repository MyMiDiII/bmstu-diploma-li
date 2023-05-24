import wget

def main():
    url = "https://download.geofabrik.de/russia/central-fed-district-latest.osm.pbf"
    wget.download(url, "./crimean-fed-district-latest.osm.pbf")

if __name__ == "__main__":
    main()
