export type LampType = string

export interface LampRecord {
  id: number
  householdId: number
  memberId: number
  memberName: string
  lampType: LampType
  year: number
  isPaid: boolean
  amount: number
  notes: string
  createdAt: string
  updatedAt: string
}

export interface HouseholdLampSummary {
  householdId: number
  phone: string
  mobile: string
  members: {
    memberId: number
    memberName: string
    lamps: LampRecord[]
  }[]
}

export interface LampRosterEntry {
  memberName: string
  lampType: LampType
  year: number
  isPaid: boolean
  amount: number
  householdPhone: string
}

export interface LampStripEntry {
  memberName: string
  lampType: LampType
  year: number
}

export interface LampQueryParams {
  year?: number
  memberName?: string
  householdId?: number
  lampType?: LampType
  page?: number
  pageSize?: number
}

export interface CreateLampPayload {
  householdId: number
  memberId: number
  lampType: LampType
  year: number
  amount: number
  isPaid: boolean
  notes?: string
}

export type UpdateLampPayload = Partial<CreateLampPayload>

export interface RosterQueryParams {
  year: number
  lampType?: LampType
  page?: number
  pageSize?: number
}

export interface StripQueryParams {
  year: number
  lampType?: LampType
}

export interface ExportParams {
  year: number
  lampType?: LampType
  format?: 'xlsx' | 'csv'
}
