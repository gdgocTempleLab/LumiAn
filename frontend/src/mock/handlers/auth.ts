import type MockAdapter from 'axios-mock-adapter'

export function setupAuthMocks(mock: MockAdapter) {
  // POST /api/auth/login
  mock.onPost('/auth/login').reply((config) => {
    const { account, password } = JSON.parse(config.data)
    if (account === 'admin' && password === 'admin123') {
      return [200, {
        token: 'mock-jwt-token-admin',
        user: { id: 1, account: 'admin', name: '管理員', role: 'admin' },
      }]
    }
    return [401, { message: '帳號或密碼錯誤' }]
  })

  // POST /api/auth/logout
  mock.onPost('/auth/logout').reply(200, { success: true })

  // GET /api/auth/me
  mock.onGet('/auth/me').reply(200, {
    id: 1, account: 'admin', name: '管理員', role: 'admin',
  })
}
