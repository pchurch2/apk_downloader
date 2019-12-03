// Search top free apps by category
var gplay = require('google-play-scraper');

const args = process.argv.slice(2);
const arg1_category = args[0];
const arg2_collection = args[1];
const arg3_number = args[2];

gplay.list({
    category: arg1_category,
    collection: gplay.collection.arg2_collection,
    num: arg3_number,
    throttle: 10
}).then(console.log, console.log);

