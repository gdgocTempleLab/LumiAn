export type CalendarType = 'lunar' | 'solar'
export type MemberRole = 'head' | 'member'

export interface Birthday {
  calendarType: CalendarType
  year: number
  month: number
  day: number
}

export interface Member {
  id: number
  householdId: number
  name: string
  role: MemberRole
  birthday: Birthday
  createdAt: string
  updatedAt: string
}

export interface Address {
  countyCode: string
  countyName: string
  districtCode: string
  districtName: string
  villageCode?: string
  villageName?: string
  detail: string
}

export interface Household {
  id: number
  phoneAreaCode: string
  phoneNumber: string
  mobile: string
  registeredAddress: Address
  residenceAddress: Address
  sameAsRegistered: boolean
  members: Member[]
  createdAt: string
  updatedAt: string
}

export interface CreateMemberPayload {
  name: string
  role: MemberRole
  birthday: Birthday
}

export interface CreateHouseholdPayload {
  phoneAreaCode: string
  phoneNumber: string
  mobile: string
  registeredAddress: Omit<Address, 'countyName' | 'districtName' | 'villageName'>
  residenceAddress: Omit<Address, 'countyName' | 'districtName' | 'villageName'>
  sameAsRegistered: boolean
  members: CreateMemberPayload[]
}

export type UpdateHouseholdPayload = Partial<CreateHouseholdPayload>
export type UpdateMemberPayload = Partial<CreateMemberPayload>

export interface HouseholdQueryParams {
  searchMethod?: 'phone' | 'name' | 'mobile'
  searchText?: string
  page?: number
  pageSize?: number
}
