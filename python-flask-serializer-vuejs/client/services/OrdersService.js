import Api from '@/services/Api'

export default {
  getAll (token) {
    return Api().get('pedidos/getAll/' + token)
  },

  get (id, token) {
    return Api().get('pedidos/get/' + id + '/' + token)
  },

  confirm (order, token) {
    return Api().post('pedidos/confirmarRecebimento', order, token)
  }
}
