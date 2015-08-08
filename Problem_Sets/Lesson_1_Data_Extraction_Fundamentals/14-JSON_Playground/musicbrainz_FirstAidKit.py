# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    results = query_by_name(ARTIST_URL, query_type["simple"], "queen")
    pretty_print(results)

    with open("Output0.txt", "w") as text_file:
        text_file.write(json.dumps(results, sort_keys=True, indent=2))

    artist_id = results["artists"][0]["id"]
    print "\nartist_id: ", artist_id
    results["artists"][0]
    
    print "\nARTIST:"
    pretty_print(results["artists"][0])

    artist_data = query_site(ARTIST_URL, query_type["atr"], artist_id)
    releases = artist_data["aliases"]
    print "\nONE RELEASE:"
    pretty_print(releases[0], indent=2)
    release_titles = [r["name"] for r in releases]

    print "\nALL TITLES:"
    for t in release_titles:
        print t

if __name__ == '__main__':
    main()
