import Vue from 'vue'
import Router from 'vue-router'
import Root from '@/components/Root'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Sales from '@/components/Sales'
import Orders from '@/components/orders/Orders'
import CreateOrder from '@/components/orders/CreateOrder'
import ViewOrder from '@/components/orders/ViewOrder'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'root',
      component: Root
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/orders',
      name: 'orders',
      component: Orders
    },
    {
      path: '/orders/:orderId',
      name: 'order',
      component: ViewOrder
    },
    {
      path: '/orders/create',
      name: 'orders-create',
      component: CreateOrder
    },
    {
      path: '/sales',
      name: 'sales',
      component: Sales
    }
  ]
})
