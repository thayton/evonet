# evonet
Prelim scraping for estimate

# Setup
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ mkdir results/
  
# Usage
    usage: concurrent_scraper.py [-h] -d PLUGIN_DIRECTORY 
                                 [-i PLUGIN_REGEXP]
                                 [-r RESULTS_DIR] 
                                 [-p MAX_PROCESSES]

You must specify the plugin directory containing the agent scrapers (eg. 'agents/')

You may optionally specify a regular expression pattern (-i) to limit which agents are loaded. The 
regular expression will apply to the filename.

You may optionally specify the directory into which the results files will be placed. The 
default is ./results/

You may optionally specify the number of agents to run concurrently. The default is 5.

# Examples
## Run all of the agents
    $ ./concurrent_scraper.py -d agents/      

## Run all of the agents
    $ ./concurrent_scraper.py -d agents/ -i '.*'

## Run only agents whose filename begins with the string 'wei'
    $ ./concurrent_scraper.py -d agents/ -i '^wei'

## Run 10 agents at the same time
    $ ./concurrent_scraper.py -d agents/ -p 10

## Put the results in directory foobar/
    $ ./concurrent_scraper.py -d agents/ -r foobar/