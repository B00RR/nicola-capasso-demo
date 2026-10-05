/* Due famiglie locali: percorsi relativi al loader, validi anche su GitHub Pages. */
const fontDirectory = new URL('.', document.currentScript.src);
const localFonts = [
  new FontFace('Italiana', `url("${new URL('italiana-regular.ttf', fontDirectory).href}")`,
    { weight: '400', style: 'normal', display: 'swap' }),
  new FontFace('Space Grotesk', `url("${new URL('space-grotesk.ttf', fontDirectory).href}")`,
    { weight: '300 700', style: 'normal', display: 'swap' })
];
window.typographyReady = Promise.all(localFonts.map(font => {
  document.fonts.add(font);
  return font.load();
}));
