# evonet
Prelim scraping for estimate

# Setup
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

# Usage
    usage: scraper.py [-h] -d PLUGIN_DIRECTORY [-r PLUGIN_REGEXP]

You must specify the plugin directory containing the agent scrapers (eg. 'agents/')

You may optionally specify a regular expression pattern to limit which agents are loaded.
The regular expression will apply to the filename.

# Examples
## Run all of the agents
    $ ./scraper.py -d agents/      

## Run all of the agents
    $ ./scraper.py -d agents/ -r '.*'

## Run only agents whose filename begins with the string 'wei'
    $ ./scraper.py -d agents/ -r '^wei'