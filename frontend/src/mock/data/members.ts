import type { Household } from '@/types'

export const mockHouseholds: Household[] = [
  {
    id: 1,
    phoneAreaCode: '04',
    phoneNumber: '25123456',
    mobile: '0912345678',
    sameAsRegistered: true,
    registeredAddress: {
      countyCode: '400', countyName: '台中市',
      districtCode: '420', districtName: '豐原區',
      villageName: '西湳里', detail: '3鄰豐北街248號',
    },
    residenceAddress: {
      countyCode: '400', countyName: '台中市',
      districtCode: '420', districtName: '豐原區',
      villageName: '西湳里', detail: '3鄰豐北街248號',
    },
    members: [
      {
        id: 1, householdId: 1, name: '羅XX', role: 'head',
        birthday: { calendarType: 'solar', year: 2001, month: 1, day: 6 },
        createdAt: '2024-01-01', updatedAt: '2024-01-01',
      },
      {
        id: 2, householdId: 1, name: '楊XX', role: 'member',
        birthday: { calendarType: 'solar', year: 2003, month: 6, day: 18 },
        createdAt: '2024-01-01', updatedAt: '2024-01-01',
      },
    ],
    createdAt: '2024-01-01',
    updatedAt: '2024-01-01',
  },
  {
    id: 2,
    phoneAreaCode: '04',
    phoneNumber: '25987654',
    mobile: '0923456789',
    sameAsRegistered: false,
    registeredAddress: {
      countyCode: '400', countyName: '台中市',
      districtCode: '420', districtName: '豐原區',
      villageName: '北湳里', detail: '中正路100號',
    },
    residenceAddress: {
      countyCode: '400', countyName: '台中市',
      districtCode: '406', districtName: '北屯區',
      villageName: '舊社里', detail: '北屯路200號',
    },
    members: [
      {
        id: 3, householdId: 2, name: '陳XX', role: 'head',
        birthday: { calendarType: 'lunar', year: 1975, month: 3, day: 15 },
        createdAt: '2024-02-01', updatedAt: '2024-02-01',
      },
      {
        id: 4, householdId: 2, name: '林XX', role: 'member',
        birthday: { calendarType: 'solar', year: 1978, month: 8, day: 22 },
        createdAt: '2024-02-01', updatedAt: '2024-02-01',
      },
      {
        id: 5, householdId: 2, name: '陳OO', role: 'member',
        birthday: { calendarType: 'solar', year: 2005, month: 11, day: 3 },
        createdAt: '2024-02-01', updatedAt: '2024-02-01',
      },
    ],
    createdAt: '2024-02-01',
    updatedAt: '2024-02-01',
  },
  {
    id: 3,
    phoneAreaCode: '04',
    phoneNumber: '25111222',
    mobile: '0934567890',
    sameAsRegistered: true,
    registeredAddress: {
      countyCode: '400', countyName: '台中市',
      districtCode: '420', districtName: '豐原區',
      villageName: '豐原里', detail: '圓環東路50號',
    },
    residenceAddress: {
      countyCode: '400', countyName: '台中市',
      districtCode: '420', districtName: '豐原區',
      villageName: '豐原里', detail: '圓環東路50號',
    },
    members: [
      {
        id: 6, householdId: 3, name: '王XX', role: 'head',
        birthday: { calendarType: 'lunar', year: 1960, month: 12, day: 8 },
        createdAt: '2024-03-01', updatedAt: '2024-03-01',
      },
    ],
    createdAt: '2024-03-01',
    updatedAt: '2024-03-01',
  },
]
