import type { TDocumentDefinitions } from 'pdfmake/interfaces'
import type { LampStripEntry } from '@/types'

export function buildStripPdfDefinition(
  data: LampStripEntry[],
  options: { year: number; lampType?: string },
): TDocumentDefinitions {
  const title = `八卦禪寺 ${options.year} 年度 燈條名單`
  const subtitle = options.lampType ? `（${options.lampType}）` : ''
  const today = new Date().toLocaleDateString('zh-TW')

  const headerRow = ['序號', '姓名', '燈種', '年度']

  const bodyRows = data.map((item, index) => [
    { text: String(index + 1), alignment: 'center' as const },
    { text: item.memberName },
    { text: item.lampType, alignment: 'center' as const },
    { text: String(item.year), alignment: 'center' as const },
  ])

  return {
    defaultStyle: {
      font: 'NotoSansTC',
      fontSize: 12,
    },
    pageSize: 'A4',
    pageMargins: [40, 40, 40, 40],
    content: [
      {
        text: title,
        fontSize: 18,
        bold: true,
        alignment: 'center',
        margin: [0, 0, 0, subtitle ? 4 : 16],
      },
      ...(subtitle
        ? [
            {
              text: subtitle,
              fontSize: 14,
              alignment: 'center' as const,
              margin: [0, 0, 0, 16] as [number, number, number, number],
            },
          ]
        : []),
      {
        table: {
          headerRows: 1,
          widths: [40, '*', 100, 60],
          body: [
            headerRow.map((h) => ({
              text: h,
              bold: true,
              alignment: 'center' as const,
              fillColor: '#F5F5F5',
            })),
            ...bodyRows,
          ],
        },
        layout: {
          hLineWidth: () => 0.5,
          vLineWidth: () => 0.5,
          hLineColor: () => '#CCCCCC',
          vLineColor: () => '#CCCCCC',
          paddingLeft: () => 8,
          paddingRight: () => 8,
          paddingTop: () => 6,
          paddingBottom: () => 6,
        },
      },
      {
        text: `共 ${data.length} 筆`,
        margin: [0, 12, 0, 4],
        fontSize: 11,
        color: '#666666',
      },
      {
        text: `列印日期：${today}`,
        fontSize: 11,
        color: '#666666',
      },
    ],
  }
}
