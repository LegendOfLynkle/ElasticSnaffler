# ElasticSnaffler

Taking Snaffler analysis to the *next* level using ElasticSearch

***

## Installation
Simply run:
```bash
pip install -r requirements.txt
```

## Usage
Supported arguments are as follows:
```text
usage: snafflemonster.py [-h] -f FILE -n HOSTNAME [-i INDEX] [-k APIKEY] [-r REPLACE] [-a APPEND] [--insecure INSECURE]

Send Snaffler Output to ElasticSearch for analysis.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The path to the JSON file to process.
  -n HOSTNAME, --hostname HOSTNAME
                        Hostname or IP pointing to the ElasticSearch instance.
  -i INDEX, --index INDEX
                        The name of the index to store results in.
  -k APIKEY, --apikey APIKEY
                        The API key used to authentiate to ElasticSearch.
  -r REPLACE, --replace REPLACE
                        Optional argument to delete existing items in the index selected before adding new items.
  -a APPEND, --append APPEND
                        Optional argument to append new items to the selected index.
  --insecure INSECURE   Toggle for allowing sending over HTTPS with verification turned off so self signed or invalid ceritficates can be used.

Happy Snaffling
```

The following is an example of using the program:
```bash
python3 snafflemonster.py -f /Path/To/Snaffler.json -n elasticsearch.snaffler.com
```

If necessary arguments such as Index and Apikey are not provided then the user will be prompted for these values at runtime.

## Support
Please contact Lynkle if you have issues.

## Authors and acknowledgment
Lynkle

## License
This project is license under the MIT license.