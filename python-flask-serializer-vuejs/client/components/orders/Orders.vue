<template>
  <v-layout justify-center>
    <v-flex xs12 sm8>
      
      <div class="white elevation-2">

        <v-toolbar flat dense class="red darken-3" dark>
          <v-toolbar-title> Pedidos </v-toolbar-title>
          
          <v-spacer></v-spacer>
          
          <v-toolbar-items>
            <v-btn @click="navigateTo({name: 'orders-create'})" outline dark class="red darken-3" >Novo Pedido</v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers" :items="orders" hide-actions class="elevation-1">
          <template slot="items" slot-scope="props">
            <td>#{{ props.item.codigo }}</td>
            <td>{{ props.item.dataEntregaEsperada }}</td>
            <v-btn small @click="navigateTo({
              name: 'order',
              params: {
                orderId: props.item.codigo
              }
              })"> Ver Detalhes</v-btn>
          </template>
        </v-data-table>

      </div>
    </v-flex>
  </v-layout>
</template>
      


<script>
import OrdersService from '@/services/OrdersService'

export default {
  data () {
    return {
      orders: [],
      headers: [
        { text: 'Código', value: 'codigo', sortable: false, align: 'center'},
        { text: 'Data de Entrega Esperada', value: 'dataEntregaEsperada', sortable: true, align: 'center' },
        { text: 'Ver Detalhes', value: 'verDetalhes', sortable: false, align: 'center' }
      ]
    }
  },
  methods: {
    navigateTo (route) {
      this.$router.push(route)
    }
  },
  
  async mounted () {
    let response = await OrdersService.getAll(this.$store.state.token)
    this.orders = response.data;
  }
}
</script>