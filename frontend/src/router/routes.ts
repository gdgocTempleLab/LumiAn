import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false, title: '登入' },
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true, title: '首頁' },
  },
  // 信徒管理
  {
    path: '/member/create',
    name: 'MemberCreate',
    component: () => import('@/views/member/MemberCreateView.vue'),
    meta: { requiresAuth: true, title: '建立信徒資料' },
  },
  {
    path: '/member/edit',
    name: 'MemberEdit',
    component: () => import('@/views/member/MemberEditView.vue'),
    meta: { requiresAuth: true, title: '編輯信徒資料' },
  },
  {
    path: '/member/delete',
    name: 'MemberDelete',
    component: () => import('@/views/member/MemberDeleteView.vue'),
    meta: { requiresAuth: true, title: '刪除信徒資料' },
  },
  {
    path: '/member/query',
    name: 'MemberQuery',
    component: () => import('@/views/member/MemberQueryView.vue'),
    meta: { requiresAuth: true, title: '查詢信徒資料' },
  },
  {
    path: '/member/list',
    name: 'MemberList',
    component: () => import('@/views/member/MemberListView.vue'),
    meta: { requiresAuth: true, title: '戶口列表' },
  },
  // 點燈管理
  {
    path: '/lamp/query',
    name: 'LampQuery',
    component: () => import('@/views/lamp/LampQueryView.vue'),
    meta: { requiresAuth: true, title: '查詢點燈資訊' },
  },
  {
    path: '/lamp/edit',
    name: 'LampEditList',
    component: () => import('@/views/lamp/LampEditListView.vue'),
    meta: { requiresAuth: true, title: '點燈紀錄' },
  },
  {
    path: '/lamp/edit/:householdId',
    name: 'LampEdit',
    component: () => import('@/views/lamp/LampEditView.vue'),
    meta: { requiresAuth: true, title: '編輯點燈' },
    props: true,
  },
  {
    path: '/lamp/roster',
    name: 'LampRoster',
    component: () => import('@/views/lamp/LampRosterView.vue'),
    meta: { requiresAuth: true, title: '查詢點燈清冊' },
  },
  {
    path: '/lamp/strip',
    name: 'LampStrip',
    component: () => import('@/views/lamp/LampStripView.vue'),
    meta: { requiresAuth: true, title: '查詢燈條名單' },
  },
  {
    path: '/lamp/export',
    name: 'LampExport',
    component: () => import('@/views/lamp/LampExportView.vue'),
    meta: { requiresAuth: true, title: '點燈' },
  },
  {
    path: '/lamp/print-form',
    name: 'LampPrintForm',
    component: () => import('@/views/lamp/LampPrintFormView.vue'),
    meta: { requiresAuth: true, title: '列印報名表' },
  },
  {
    path: '/lamp/print-strip',
    name: 'LampPrintStrip',
    component: () => import('@/views/lamp/LampPrintStripView.vue'),
    meta: { requiresAuth: true, title: '列印燈條' },
  },
  // 帳號管理
  {
    path: '/account',
    name: 'AccountManage',
    component: () => import('@/views/account/AccountManageView.vue'),
    meta: { requiresAuth: true, title: '帳號管理' },
  },
  // Catch-all
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]
