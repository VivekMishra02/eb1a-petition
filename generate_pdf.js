const puppeteer = require('puppeteer');
(async () => {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto('https://voyagela.com/interview/rising-stars-meet-vivek-mishra-of-long-beach/', { waitUntil: 'networkidle2' });
        await page.pdf({
            path: '/Users/vivekmishra/Downloads/eb1_template/criteria/media/evidence/VoyageLA_Interview.pdf',
            format: 'A4',
            printBackground: true,
            margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' }
        });
        await browser.close();
        console.log('PDF saved successfully');
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
})();
