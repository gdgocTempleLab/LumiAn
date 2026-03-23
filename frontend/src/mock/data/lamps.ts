import type { LampRecord } from '@/types'

export const mockLampRecords: LampRecord[] = [
  {
    id: 1, householdId: 1, memberId: 1, memberName: '羅XX',
    lampType: '光明燈', year: 2026, isPaid: true, amount: 500,
    notes: '', createdAt: '2026-01-15', updatedAt: '2026-01-15',
  },
  {
    id: 2, householdId: 1, memberId: 1, memberName: '羅XX',
    lampType: '太歲燈', year: 2026, isPaid: true, amount: 600,
    notes: '', createdAt: '2026-01-15', updatedAt: '2026-01-15',
  },
  {
    id: 3, householdId: 1, memberId: 2, memberName: '楊XX',
    lampType: '光明燈', year: 2026, isPaid: false, amount: 500,
    notes: '尚未繳費', createdAt: '2026-01-15', updatedAt: '2026-01-15',
  },
  {
    id: 4, householdId: 2, memberId: 3, memberName: '陳XX',
    lampType: '光明燈', year: 2026, isPaid: true, amount: 500,
    notes: '', createdAt: '2026-02-01', updatedAt: '2026-02-01',
  },
  {
    id: 5, householdId: 2, memberId: 3, memberName: '陳XX',
    lampType: '藥師燈', year: 2026, isPaid: true, amount: 800,
    notes: '', createdAt: '2026-02-01', updatedAt: '2026-02-01',
  },
  {
    id: 6, householdId: 2, memberId: 4, memberName: '林XX',
    lampType: '光明燈', year: 2026, isPaid: true, amount: 500,
    notes: '', createdAt: '2026-02-01', updatedAt: '2026-02-01',
  },
  {
    id: 7, householdId: 3, memberId: 6, memberName: '王XX',
    lampType: '光明燈', year: 2025, isPaid: true, amount: 500,
    notes: '', createdAt: '2025-01-10', updatedAt: '2025-01-10',
  },
  {
    id: 8, householdId: 3, memberId: 6, memberName: '王XX',
    lampType: '太歲燈', year: 2025, isPaid: true, amount: 600,
    notes: '', createdAt: '2025-01-10', updatedAt: '2025-01-10',
  },
]
