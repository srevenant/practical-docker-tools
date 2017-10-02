const Browser = require('zombie');
url = 'http://phoenix:4000/';
browser = new Browser();

describe("test phoenix hello", function() {
    it("should have defined headless browser", function(next) {
        expect(typeof browser != "undefined").toBe(true);
        expect(browser instanceof Browser).toBe(true);
        next();
    });

    it("should visit the site", function(next) {
        browser.visit(url, function(err) {
            expect(browser.success).toBe(true);
            expect(browser.html("body")).toContain("Welcome to Phoenix");
            next();
        })
    });

});

