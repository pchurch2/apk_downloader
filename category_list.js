// Lists all available categories

var gplay = require('google-play-scraper');

gplay.categories({
    throttle: 10
}).then(console.log);
