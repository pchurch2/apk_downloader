# apk_downloader
APK Downloader for the Google Play Store

---

&nbsp;

### Prerequisites

---

#### Node Version Manager (NVM)

Requires Node.js.  Follow the Install Script instructions at [GitHub - NVM](https://github.com/nvm-sh/nvm#installation-and-update) with curl or wget:

```sh
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash
```

```sh
$ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash
```

Close and restart the terminal and verify installation was successful:

```sh
$ command -v nvm
```

Download, compile, and install the latest release of Node:

```sh
$ nvm install node
```

Start Node:
```sh
$ nvm use node
```

&nbsp;

#### Google-Play-Scraper

Requires Google-Play-Scraper.  Follow the install instructions at [GitHub - Google-Play-Scraper](https://github.com/facundoolano/google-play-scraper):
```sh
$ npm install google-play-scraper
```

&nbsp;

#### Naked Python Tool

Requires the Naked Python Tool.  Follow the install instructions at [Naked Python Tool](https://sweetme.at/2014/02/17/a-simple-approach-to-execute-a-node.js-script-from-python/):
```sh
$ pip3 install naked
```

&nbsp;

### Installation and Usage

---

The following files are required:
* apk_download.py
  * Python 3 script to retreive app_ids and download APKs
* app_list.js
  * Node file used to scrape app_ids from the Google Play Store
* category_list.js
  * Node file used to scrape categories from the Google Play Store

Run the apk_download.py tool:
```sh
$ python3 apk_download.py
```

By default, the apk_downloader will use the TOP_FREE collection and find 5 app_ids from each category currently available on the Google Play Store.  These variables can be modified in apk_download.py:

```
collection_type = "TOP_FREE"
app_per_category = "5"
```

&nbsp;

### TODO

---

- Get a working APK downloader:
- [GPlayDL](https://github.com/rehmatworks/gplaydl) was initially working but now getting _Login Failure_ errors during runtime.
- Will attempt to get [GooglePlay-API](https://github.com/NoMore201/googleplay-api) to work.
