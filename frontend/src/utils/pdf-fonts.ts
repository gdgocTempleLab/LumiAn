import pdfMake from 'pdfmake/build/pdfmake'

let fontsLoaded = false

export async function getPdfMake() {
  if (fontsLoaded) return pdfMake

  const response = await fetch('/fonts/NotoSansTC.ttf')
  const buffer = await response.arrayBuffer()
  const bytes = new Uint8Array(buffer)
  const chunks: string[] = []
  const chunkSize = 0x8000
  for (let i = 0; i < bytes.length; i += chunkSize) {
    chunks.push(String.fromCharCode(...bytes.subarray(i, i + chunkSize)))
  }
  const base64 = btoa(chunks.join(''))

  pdfMake.addFontContainer({
    vfs: { 'NotoSansTC.ttf': base64 },
    fonts: {
      NotoSansTC: {
        normal: 'NotoSansTC.ttf',
        bold: 'NotoSansTC.ttf',
        italics: 'NotoSansTC.ttf',
        bolditalics: 'NotoSansTC.ttf',
      },
    },
  })

  fontsLoaded = true
  return pdfMake
}
