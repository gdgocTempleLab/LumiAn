import type MockAdapter from 'axios-mock-adapter'
import { mockHouseholds } from '../data/members'
import type { Household } from '@/types'

let households = [...mockHouseholds]
let nextId = 100
let nextMemberId = 100

export function setupMemberMocks(mock: MockAdapter) {
  // GET /api/households - 查詢
  mock.onGet('/households').reply((config) => {
    const params = config.params || {}
    let filtered = [...households]

    if (params.searchText) {
      const text = params.searchText
      switch (params.searchMethod) {
        case 'phone':
          filtered = filtered.filter((h) =>
            `${h.phoneAreaCode}${h.phoneNumber}`.includes(text),
          )
          break
        case 'mobile':
          filtered = filtered.filter((h) => h.mobile.includes(text))
          break
        case 'name':
          filtered = filtered.filter((h) =>
            h.members.some((m) => m.name.includes(text)),
          )
          break
      }
    }

    return [200, {
      success: true,
      data: filtered,
      total: filtered.length,
      page: 1,
      pageSize: 10,
    }]
  })

  // GET /api/households/:id
  mock.onGet(/\/households\/\d+/).reply((config) => {
    const id = parseInt(config.url!.split('/').pop()!)
    const household = households.find((h) => h.id === id)
    if (household) {
      return [200, { success: true, data: household }]
    }
    return [404, { success: false, message: '找不到資料' }]
  })

  // POST /api/households - 建立
  mock.onPost('/households').reply((config) => {
    const data = JSON.parse(config.data)
    const newHousehold: Household = {
      id: nextId++,
      ...data,
      members: data.members.map((m: Record<string, unknown>) => ({
        id: nextMemberId++,
        householdId: nextId - 1,
        ...m,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      })),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    households.push(newHousehold)
    return [200, { success: true, data: newHousehold, message: '建立成功' }]
  })

  // PUT /api/households/:id - 更新
  mock.onPut(/\/households\/\d+/).reply((config) => {
    const id = parseInt(config.url!.split('/').pop()!)
    const index = households.findIndex((h) => h.id === id)
    if (index >= 0) {
      const data = JSON.parse(config.data)
      households[index] = { ...households[index], ...data, updatedAt: new Date().toISOString() }
      return [200, { success: true, data: households[index], message: '更新成功' }]
    }
    return [404, { success: false, message: '找不到資料' }]
  })

  // DELETE /api/households/:id
  mock.onDelete(/\/households\/\d+/).reply((config) => {
    const id = parseInt(config.url!.split('/').pop()!)
    households = households.filter((h) => h.id !== id)
    return [200, { success: true, message: '刪除成功' }]
  })

  // POST /api/households/:id/members - 新增戶員
  mock.onPost(/\/households\/\d+\/members/).reply((config) => {
    const parts = config.url!.split('/')
    const householdId = parseInt(parts[parts.length - 2])
    const household = households.find((h) => h.id === householdId)
    if (household) {
      const data = JSON.parse(config.data)
      household.members.push({
        id: nextMemberId++,
        householdId,
        ...data,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      })
      return [200, { success: true, message: '新增成功' }]
    }
    return [404, { success: false, message: '找不到戶口' }]
  })

  // DELETE /api/members/:id
  mock.onDelete(/\/members\/\d+/).reply((config) => {
    const memberId = parseInt(config.url!.split('/').pop()!)
    for (const h of households) {
      h.members = h.members.filter((m) => m.id !== memberId)
    }
    return [200, { success: true, message: '刪除成功' }]
  })
}
