import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MainLayout from '@/layout/MainLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/LoginView.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/main',
    component: MainLayout,
    redirect: '/main/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
        meta: {
          title: '仪表盘',
          icon: 'Monitor',
          requiresAuth: true
        }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/UserListView.vue'),
        meta: {
          title: '用户管理',
          icon: 'User',
          requiresAuth: true
        }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/products/ProductListView.vue'),
        meta: {
          title: '产品管理',
          icon: 'Goods',
          requiresAuth: true
        }
      },
      {
        path: 'inventory',
        name: 'Inventory',
        component: () => import('@/views/inventory/InventoryView.vue'),
        meta: {
          title: '库存管理',
          icon: 'Box',
          requiresAuth: true
        }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/views/orders/OrderListView.vue'),
        meta: {
          title: '订单管理',
          icon: 'List',
          requiresAuth: true
        }
      },
      {
        path: 'suppliers',
        name: 'Suppliers',
        component: () => import('@/views/suppliers/SupplierListView.vue'),
        meta: {
          title: '供应商管理',
          icon: 'Connection',
          requiresAuth: true
        }
      },
      {
        path: 'nlp',
        name: 'NLP',
        component: () => import('@/views/nlp/NLPView.vue'),
        meta: {
          title: '自然语言处理',
          icon: 'ChatDotRound',
          requiresAuth: true
        }
      },
      {
        path: 'finance',
        name: 'Finance',
        component: () => import('@/views/finance/FinanceView.vue'),
        redirect: '/main/finance/accounts',
        meta: {
          title: '财务管理',
          icon: 'Money',
          requiresAuth: true
        },
        children: [
          {
            path: 'accounts',
            name: 'Accounts',
            component: () => import('@/views/finance/AccountView.vue'),
            meta: {
              title: '账户管理',
              requiresAuth: true
            }
          },
          {
            path: 'transactions',
            name: 'Transactions',
            component: () => import('@/views/finance/TransactionView.vue'),
            meta: {
              title: '交易记录',
              requiresAuth: true
            }
          },
          {
            path: 'budgets',
            name: 'Budgets',
            component: () => import('@/views/finance/BudgetView.vue'),
            meta: {
              title: '预算管理',
              requiresAuth: true
            }
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  // 设置页面标题
  document.title = `${to.meta.title || 'ERP系统'}`

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
