from uniform import generate_uniform
from normal import generate_normal
from osm.generate_csv import generate_osm

def generate_data():
    print("UNIFORM")
    generate_uniform()

    print("NORMAL")
    generate_normal()

    print("OSM")
    generate_osm()

if __name__ == "__main__":
    generate_data()
