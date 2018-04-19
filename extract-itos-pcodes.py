"""Extract P-codes from iTOS and export as CSV"""
import csv, logging, requests, sys

if sys.version_info < (3,):
    raise RuntimeError("Requires Python3")

logger = logging.getLogger(__name__)

#
# Constants
#

URL_PATTERN = 'http://gistmaps.itos.uga.edu/arcgis/rest/services/COD_External/{country}_pcode/MapServer/{level}/query?where=1%3D1&outFields=*&returnGeometry=false&f=pjson'
"""Pattern for constructing an iTOS query URL."""

COLUMN_SPECS = {
    "admin0RefName": "#country+name+i_en",
    "admin0Name_fr": "#country+name+i_fr",
    "admin0Pcode": "#country+code",
    "admin1RefName": "#adm1+name+i_en",
    "admin1Name_fr": "#adm1+name+i_fr",
    "admin1Pcode": "#adm1+code",
    "admin2RefName": "#adm2+name+i_en",
    "admin2Name_fr": "#adm2+name+i_fr",
    "admin2Pcode": "#adm2+code",
    "admin3RefName": "#adm3+name+i_en",
    "admin3Name_fr": "#adm3+name+i_fr",
    "admin3Pcode": "#adm3+code",
    "admin4RefName": "#adm4+name+i_en",
    "admin4Name_fr": "#adm4+name+i_fr",
    "admin4Pcode": "#adm4+code",
    "admin5RefName": "#adm5+name+i_en",
    "admin5Name_fr": "#adm5+name+i_fr",
    "admin5Pcode": "#adm5+code",
}
"""Map of iTOS headers to HXL hashtags."""

#
# Functions
#

def extract_pcodes(country, level, fp):
    """Extract P-codes to HXL-hashtagged CSV
    @param country: an ISO3 country code
    @param level: the admin level (1=country)
    @param fp: a file-like object (with a .write() method)
    """

    url = URL_PATTERN.format(country=country.upper(), level=int(level))

    with requests.get(url) as result:
        output = csv.writer(sys.stdout)
        data = result.json()

        if "error" in data:
            raise Exception(data['error']['message'])

        # Set up the header and hashtag rows
        headers = []
        for header in COLUMN_SPECS:
            for field in data['fields']:
                if field['name'] == header:
                    headers.append(header)
        hashtags = [COLUMN_SPECS[header] for header in headers]

        # Print the headers and hashtags
        output.writerow(headers)
        output.writerow(hashtags)

        # Process the rows
        for entry in data['features']:
            row = []
            for header in COLUMN_SPECS:
                # only fields in the header row get included
                if header in entry['attributes']:
                    row.append(entry['attributes'][header])
            output.writerow(row)


# Run from command line
if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.error("Usage: %s <country code> <level>", sys.argv[0])
        sys.exit(1)
    name, country, level = sys.argv

    try:
        extract_pcodes(country, level, sys.stdout)
    except Exception as e:
        logger.error(e)
        sys.exit(2)
        

