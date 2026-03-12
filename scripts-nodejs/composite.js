#!/usr/bin/env node

/**
 * Brand Campaign Typography Compositor
 *
 * Takes a photo-only image and composites hook text on top using
 * HTML/CSS typography rendered by Playwright.
 *
 * Usage:
 *   node composite.js --photo /path/to/photo.png --hook "The hook." --output /path/to/final.png
 *
 * Options:
 *   --photo    Path to the photo-only image (required)
 *   --hook     The hook text to render (required)
 *   --output   Output path for the composited image (required)
 *   --layout   Text position: top-left, top-right, center-top, bottom-left (default: top-left)
 *   --theme    Text color: white or dark (default: white)
 */

const { chromium } = require('playwright');
const path = require('path');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--') && i + 1 < argv.length) {
      args[argv[i].slice(2)] = argv[i + 1];
      i++;
    }
  }
  return args;
}

async function composite(args) {
  const photo  = path.resolve(args.photo);
  const hook   = args.hook;
  const layout = args.layout || 'top-left';
  const theme  = args.theme || 'white';
  const output = path.resolve(args.output);

  if (!args.photo || !args.hook || !args.output) {
    console.error('ERROR: --photo, --hook, and --output are required');
    process.exit(1);
  }

  const templatePath = path.join(__dirname, 'brand-template.html');
  const templateUrl = new URL(`file://${templatePath}`);

  // Encode the photo path as a file:// URL for the CSS background-image
  const photoFileUrl = `file://${photo}`;

  templateUrl.searchParams.set('photo', photoFileUrl);
  templateUrl.searchParams.set('hook', hook);
  templateUrl.searchParams.set('layout', layout);
  templateUrl.searchParams.set('theme', theme);

  console.log(`Photo:  ${photo}`);
  console.log(`Hook:   ${hook}`);
  console.log(`Layout: ${layout}`);
  console.log(`Theme:  ${theme}`);
  console.log(`Output: ${output}`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 1080 });

  await page.goto(templateUrl.toString(), { waitUntil: 'networkidle' });

  // Wait for the background image to fully load
  await page.waitForFunction(() => {
    return new Promise((resolve) => {
      const el = document.getElementById('container');
      const bg = getComputedStyle(el).backgroundImage;
      if (!bg || bg === 'none') { resolve(false); return; }

      const url = bg.slice(5, -2);
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => resolve(false);
      img.src = url;

      // If already cached/complete
      if (img.complete) resolve(true);
    });
  }, { timeout: 15000 });

  // Small delay to ensure rendering is complete
  await page.waitForTimeout(200);

  // Screenshot just the container element
  const container = page.locator('#container');
  await container.screenshot({ path: output });

  await browser.close();

  console.log(`\nSUCCESS: ${output}`);
}

composite(parseArgs(process.argv.slice(2))).catch((err) => {
  console.error(`FAILED: ${err.message}`);
  process.exit(1);
});
