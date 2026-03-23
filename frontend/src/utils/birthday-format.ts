import type { Birthday } from '@/types'

const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
const ZODIAC_ANIMALS = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬']
const CHINESE_NUMBERS = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

export function toChineseStemBranch(year: number): string {
  const stemIndex = (year - 4) % 10
  const branchIndex = (year - 4) % 12
  return `${HEAVENLY_STEMS[stemIndex]}${EARTHLY_BRANCHES[branchIndex]}(${ZODIAC_ANIMALS[branchIndex]})`
}

function toChineseNumber(n: number): string {
  if (n <= 10) return CHINESE_NUMBERS[n]
  if (n < 20) return `十${CHINESE_NUMBERS[n - 10]}`
  if (n === 20) return '二十'
  if (n < 30) return `二十${CHINESE_NUMBERS[n - 20]}`
  return `三十${CHINESE_NUMBERS[n - 30]}`
}

export function toChineseMonth(month: number): string {
  return `${toChineseNumber(month)}月`
}

export function toChineseDay(day: number): string {
  return `${toChineseNumber(day)}日`
}

export function formatBirthday(birthday: Birthday): string {
  const stemBranch = toChineseStemBranch(birthday.year)
  const month = toChineseMonth(birthday.month)
  const day = toChineseDay(birthday.day)
  return `${stemBranch}\u3000${month}\u3000${day}`
}
