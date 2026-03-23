import MockAdapter from 'axios-mock-adapter'
import apiClient from '@/api/client'
import { setupAuthMocks } from './handlers/auth'
import { setupMemberMocks } from './handlers/member'
import { setupLampMocks } from './handlers/lamp'

export function setupMocks() {
  const mock = new MockAdapter(apiClient, { delayResponse: 300 })
  setupAuthMocks(mock)
  setupMemberMocks(mock)
  setupLampMocks(mock)
}
