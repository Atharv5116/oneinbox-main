import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/oneinbox',
    name: 'Inbox',
    component: () => import('@/pages/OneInbox.vue'),
    meta: { scrollPos: { top: 0, left: 0 } },
  },
  {
    path: '/:invalidpath',
    name: 'Invalid Page',
    component: () => import('@/pages/InvalidPage.vue'),
  }
]

let router = createRouter({
  history: createWebHistory('/oneinbox'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { isLoggedIn } = sessionStore()

  isLoggedIn && (await userResource.promise)

  if (from.meta?.scrollPos) {
    from.meta.scrollPos.top = document.querySelector('#list-rows')?.scrollTop
  }

  if (to.name === 'Home' && isLoggedIn) {
    next({ name: 'Inbox' })
  } else if (!isLoggedIn) {
    window.location.href = '/login?redirect-to=/oneinbox'
  } else if (to.matched.length === 0) {
    next({ name: 'Invalid Page' })
  } else {
    next()
  }
})

export default router
