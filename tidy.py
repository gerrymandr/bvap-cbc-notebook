import pandas


def tidy_cd_data():
    df = pandas.read_csv("./raw/CD.csv")

    bvap = df[df["LNNUMBER"] == 5][["GEOID", "CVAP_EST"]].set_index("GEOID")["CVAP_EST"]
    total_cvap = df[df["LNNUMBER"] == 1][["GEOID", "CVAP_EST"]].set_index("GEOID")[
        "CVAP_EST"
    ]
    total_pop = df[df["LNNUMBER"] == 1][["GEOID", "TOT_EST"]].set_index("GEOID")[
        "TOT_EST"
    ]
    black_pop = df[df["LNNUMBER"] == 5][["GEOID", "TOT_EST"]].set_index("GEOID")[
        "TOT_EST"
    ]
    display_name = df[df["LNNUMBER"] == 1][["GEOID", "GEONAME"]].set_index("GEOID")[
        "GEONAME"
    ]

    tidy_df = pandas.DataFrame(
        {
            "display_name": display_name,
            "bvap": bvap,
            "cvap": total_cvap,
            "bvap_pct": bvap / total_cvap,
            "black_pop": black_pop,
            "total_pop": total_pop,
            "black_pct": black_pop / total_pop,
        }
    )

    tidy_df.to_csv("./cvap.csv")


def assign_geoids_to_cbc_data():
    df = pandas.read_csv("./cbc.csv")
    df["GEOID"] = df["cd"].apply(parse_geoid)
    tidy_df = df.set_index("GEOID")
    tidy_df.to_csv("./cbc.csv")


def parse_geoid(cd_value):
    split_string = cd_value.split("-")
    state = split_string[0].strip()
    fips = state_name_to_fips[state]
    district = split_string[-1][:-2].strip().zfill(2)
    return "50000US" + fips + district


fips_to_state_name = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
}

state_name_to_fips = {value: key for key, value in fips_to_state_name.items()}


def main():
    tidy_cd_data()
    assign_geoids_to_cbc_data()


if __name__ == "__main__":
    main()
