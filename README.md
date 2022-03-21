# weBlock

weBlock claims to be an ad-blocker that runs on a server to save client-side processing power, but could secretly censor data at the deployer's disposal.

This is a collaborative project with [lucasliebe](https://github.com/lucasliebe) and [tiny-fish-T](https://github.com/tiny-fish-T) and is being developed within the scope of a course named *DarkAI* at [HPI](https://hpi.de). The course's goal is to raise awareness about possible harms and threats of artificial intelligence and to provoke more critical thinking in handling software products.

## Installation

This project consists of a client and server, which can be installed and run separately. Both actors require a working installation of [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/) and [Zsh](https://www.zsh.org) or [Bash](https://www.gnu.org/software/bash/). In addition, the client requires [Node.js](https://nodejs.org/en/) and [Yarn](https://yarnpkg.com) and the server requires [Python 3](https://www.python.org) together with python3-venv, [Geckodriver](https://github.com/mozilla/geckodriver/releases) (which is installed by downloading the operating system's respective executable and moving it into the `$PATH`), [Make](https://www.gnu.org/software/make/) and [GCC](https://gcc.gnu.org).

With the above requirements met, the install script can be run in `bash` or `zsh`, e.g.`./install.sh` to install both client as well as server or with an argument `client` or `server` to install only the respective actor.

## Usage

### Client

To run the client, go the the `client/` directory and run `yarn start`. This will open an instance of Firefox with the ad-blocking / censoring extension loaded. The toolbar will show weBlock's icon, where the address of your server that has weBlock's server side deployed can be set. By default, this is assumed to be `localhost`.

Browsing with the extension loaded will behave normally, but you will notice a circle icon show up on the right side of the URL field for tabs with supported webpages (http(s), html).Clicking the icon once will put the ad-blocker to work doing it's best to remove advertisements and give you a preview of what content will be censored by coloring it red. Clicking it a second time will engage censoring and replace the red text with content the censorer (server) deems as friendly but still contextually relevant.

### Server

#### Quick start with example

Run `source server/activate`, then `server/scrape-postive -t && server/scrape-negative && server/run-backend` and use the client as described above when scripts are ready (i.e. the prompt

```
setup done, waiting for connection
```

has shown up).

#### Detailed guide

Before using any of the server's functionality, `source` the `activate` file in `server/` in your `bash` or `zsh` shell. This will load the virtual environment the server lives in and greet you with the `(weBlock-server)` message in your shell's prompt.

weBlock's server side is managed by three executable scripts in the `server/` directory, namely `scrape-positive`, `scrape-negative` and `run-backend`.

##### Data collection & building models: scraping & training

For the collection of data, weBlock relies on [Google News](https://news.google.com/) to scrape recently published articles. Those articles in turn are then scraped for information used to train its natural language processing models and build a database of paragraphs used to replace censored content.

`scrape-negative` is used to collect examples for what is undesired by the censorer. It searches Google News with the comma-separated queries defined in the environment variable `NEGATIVE_QUERIES` in `server/.env`.\
The scraped articles are then used as negative examples in censoring, where the [Word Mover's Distance](http://proceedings.mlr.press/v37/kusnerb15.pdf) of a paragraph to the scraped article's summaries plays a role in determining wether that paragraph should be censored.

`scrape-positive` is used to collect examples for what is desired by the censorer. It, analogously to `scrape-negative`, searches Google News with the comma-separated queries defined in the environment variable `POSITIVE_QUERIES` in `server/.env`.\
If `scrape-positive` is run with the argument `-t` or `--train`, the resulting articles from this scraping are used to train a [Biterm Topic Model](https://github.com/xiaohuiyan/xiaohuiyan.github.io/blob/master/paper/BTM-WWW13.pdf) with the parameters defined by the environment variables `TRAINING_*` as given in `server/.env`. Leave these parameters unchanged for fast but far-from-optimal results. Training is necessary on the first run, but can later be skipped to reuse the existing BT Model.\
The Biterm Topic Model makes the key decision in finding which of the scraped positive, desired examples in the database will be used to replace a paragraph that is marked for censorship.

Both `scrape-positive` as well as `scrape-negative` have an optional argument `-n` or `--narticles` that can be used to define an upper limit for how many arguments are scraped per query. This argument defaults to `10` if omitted.

Note that Google search operators such as the `site:` or `when:` modifiers  can strongly refine and empower defined search queries (e.g. `when:7d` constrains results to articles published in the past week). See [this incomplete list of operators](https://developers.google.com/search/docs/advanced/debug/search-operators/overview).

##### Running the server

With data collection and model training done, the server now has sufficient data to act as weBlock's backend. To run the backend, execute `server/run-backend`. Once it's ready, use the client as described above.

## Scalability

Since this is a proof-of-concept prototype and focussed on the natural language processing side of the project, some features that would be significant for scalability and real-world use have been left unattended for ease of use, ease of installation, project size and human resource prioritization. These include, but are not limited to

- database & RAM: this project does not use a real database but instead simple text files and is strongly constrained by the RAM's size (e.g. the entire databases' contents may be loaded in RAM at times)
- server: the current architecture uses a simple socket for serving the (*singular*) client
- full performance optimization
- censorship of non-textual & non-html content (i.e. images, videos, documents)

## Disclaimer

As stated above, this project is aimed at raising awareness about possible harms and threats AI can pose and is therefore not intended for any malicous use or use diverging from this intention. This is also the reason why censoring does not happen in secret and "behind the scenes" as it could, but is implemented as a two step and manually triggered process on the client side and why censored and modified paragraphs are colored in red.

