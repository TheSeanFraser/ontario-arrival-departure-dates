import requests as req

ont_all_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=1900&eyr=2022&r=CA-ON&spp="
ont_20_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=2002&eyr=2022&r=CA-ON&spp="
tor_all_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=1900&eyr=2022&r=CA-ON-TO&spp="
tor_20_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=2002&eyr=2022&r=CA-ON-TO&spp="

data_url_postfix = "&fmt=tsv"


# Removes quotes from species codes
def fix_species_quotes(species):
    if "\"" in species:
        species = species[:-1]
    if "\"" in species:
        species = species[:-1]

    return species


# Downloads eBird frequency charts
def get_charts():
    species_list = open("ont_species_6letter_likely.txt", 'r').read().splitlines()

    for species in species_list:
        print("Next: " + species)
        species_fixed = fix_species_quotes(species)
        ont_all_url = ont_all_years_url + species_fixed + data_url_postfix
        ont_20_url = ont_20_years_url + species_fixed + data_url_postfix
        tor_all_url = tor_all_years_url + species_fixed + data_url_postfix
        tor_20_url = tor_20_years_url + species_fixed + data_url_postfix

        # Get data from web
        session = req.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
        r = session.get(ont_all_url)

        # Write to file
        f = open("Ontario Charts\\" + "ALL_YEARS_" + species_fixed + ".txt",
                 "w", encoding="utf-8")
        f.write(r.text)
        f.close()

        r = session.get(ont_20_url)

        # Write to file
        f = open("Ontario Charts\\" + "20_YEARS_" + species_fixed + ".txt",
                 "w", encoding="utf-8")
        f.write(r.text)
        f.close()

        r = session.get(tor_all_url)

        # Write to file
        f = open("Toronto Charts\\" + "ALL_YEARS_" + species_fixed + ".txt",
                 "w", encoding="utf-8")
        f.write(r.text)
        f.close()

        r = session.get(tor_20_url)

        # Write to file
        f = open("Toronto Charts\\" + "20_YEARS_" + species_fixed + ".txt",
                 "w", encoding="utf-8")
        f.write(r.text)
        f.close()


get_charts()
