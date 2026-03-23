import type MockAdapter from 'axios-mock-adapter'
import { mockLampRecords } from '../data/lamps'
import type { LampRecord } from '@/types'

let lamps = [...mockLampRecords]
let nextId = 100

export function setupLampMocks(mock: MockAdapter) {
  // GET /api/lamps - 查詢點燈
  mock.onGet('/lamps').reply((config) => {
    const params = config.params || {}
    let filtered = [...lamps]

    if (params.year) filtered = filtered.filter((l) => l.year === Number(params.year))
    if (params.memberName) filtered = filtered.filter((l) => l.memberName.includes(params.memberName))
    if (params.householdId) filtered = filtered.filter((l) => l.householdId === Number(params.householdId))
    if (params.lampType) filtered = filtered.filter((l) => l.lampType === params.lampType)

    return [200, {
      success: true, data: filtered, total: filtered.length, page: 1, pageSize: 50,
    }]
  })

  // GET /api/lamps/household/:id
  mock.onGet(/\/lamps\/household\/\d+/).reply((config) => {
    const householdId = parseInt(config.url!.split('/').pop()!)
    const params = config.params || {}
    let records = lamps.filter((l) => l.householdId === householdId)
    if (params.year) records = records.filter((l) => l.year === Number(params.year))

    const memberMap = new Map<number, { memberId: number; memberName: string; lamps: LampRecord[] }>()
    for (const r of records) {
      if (!memberMap.has(r.memberId)) {
        memberMap.set(r.memberId, { memberId: r.memberId, memberName: r.memberName, lamps: [] })
      }
      memberMap.get(r.memberId)!.lamps.push(r)
    }

    return [200, {
      success: true,
      data: { householdId, phone: '', mobile: '', members: Array.from(memberMap.values()) },
    }]
  })

  // POST /api/lamps
  mock.onPost('/lamps').reply((config) => {
    const data = JSON.parse(config.data)
    const newLamp: LampRecord = {
      id: nextId++, ...data,
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
    }
    lamps.push(newLamp)
    return [200, { success: true, data: newLamp }]
  })

  // PUT /api/lamps/:id
  mock.onPut(/\/lamps\/\d+/).reply((config) => {
    const id = parseInt(config.url!.split('/').pop()!)
    const index = lamps.findIndex((l) => l.id === id)
    if (index >= 0) {
      const data = JSON.parse(config.data)
      lamps[index] = { ...lamps[index], ...data, updatedAt: new Date().toISOString() }
      return [200, { success: true, data: lamps[index] }]
    }
    return [404, { success: false, message: '找不到資料' }]
  })

  // GET /api/lamps/history/:householdId
  mock.onGet(/\/lamps\/history\/\d+/).reply((config) => {
    const householdId = parseInt(config.url!.split('/').pop()!)
    const records = lamps.filter((l) => l.householdId === householdId)
    return [200, { success: true, data: records }]
  })

  // GET /api/lamps/roster
  mock.onGet('/lamps/roster').reply((config) => {
    const params = config.params || {}
    let filtered = [...lamps]
    if (params.year) filtered = filtered.filter((l) => l.year === Number(params.year))

    const roster = filtered.map((l) => ({
      memberName: l.memberName, lampType: l.lampType, year: l.year,
      isPaid: l.isPaid, amount: l.amount, householdPhone: '',
    }))
    return [200, { success: true, data: roster, total: roster.length, page: 1, pageSize: 50 }]
  })

  // GET /api/lamps/strips
  mock.onGet('/lamps/strips').reply((config) => {
    const params = config.params || {}
    let filtered = [...lamps]
    if (params.year) filtered = filtered.filter((l) => l.year === Number(params.year))

    const strips = filtered.map((l) => ({
      memberName: l.memberName, lampType: l.lampType, year: l.year,
    }))
    return [200, { success: true, data: strips }]
  })

  // GET /api/lamps/export
  mock.onGet('/lamps/export').reply(200, new Blob(['mock export data'], { type: 'text/csv' }))
}
