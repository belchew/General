const puppeteer = require('puppeteer');
const fs = require('fs');

// Канали (примерен списък – може да добавиш още)
const channelNameMapping = {
    "hd-bnt-1-hd": "BNT1",
    "bnt-2": "BNT2",
    "hd-bnt-3-hd": "BNT3",
    "bnt-4": "BNT4",
    "hd-nova-tv-hd": "Nova",
    "hd-btv-hd": "bTV",
    "hd-btv-action-hd": "bTVAction"
};

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox']
  });

  fs.writeFileSync('sources.m3u', '#EXTM3U\n', 'utf-8');

  for (const [urlPart, channelName] of Object.entries(channelNameMapping)) {
    const page = await browser.newPage();
    const m3u8Links = new Set();

    page.on('response', async (response) => {
      const url = response.url();
      if (url.includes('.m3u8')) {
        m3u8Links.add(url);
      }
    });

    const fullURL = `https://www.seir-sanduk.com/${urlPart}`;
    console.log(`⏳ Отварям: ${fullURL}`);

    try {
      await page.goto(fullURL, { waitUntil: 'networkidle2' });

      // Заместваме waitForTimeout с timeout чрез Promise
      await new Promise(resolve => setTimeout(resolve, 5000));

      if (m3u8Links.size > 0) {
        for (const link of m3u8Links) {
          const data = `#EXTINF:-1,${channelName}\n${link}\n`;
          fs.appendFileSync('sources.m3u', data, 'utf-8');
          console.log(`✅ ${channelName}: ${link}`);
        }
      } else {
        console.log(`⚠️ Не са намерени .m3u8 линкове за ${channelName}`);
      }
    } catch (err) {
      console.error(`❌ Грешка за ${channelName}: ${err.message}`);
    }

    await page.close();
  }

  await browser.close();
  console.log('\n✅ Готово! Всички намерени линкове са записани в sources.m3u');
})();
