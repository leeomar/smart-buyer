var page = require('webpage').create(),
    system = require('system'),
    t, address;

if (system.args.length === 1) {
    console.log('Usage: phantomjs_load_page.js <some URL> [output file]');
    phantom.exit(1);
} else {
    address = system.args[1];
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('FAIL to load ' + address + ', status: ' + status);
            phantom.exit(1);
        } else {
            if (system.args.length === 3) {
                var fs = require('fs');
                fs.write(system.args[2], page.content, 'w')
            } else {
                console.log(page.content)
            }
            phantom.exit();
        }
    });
}
