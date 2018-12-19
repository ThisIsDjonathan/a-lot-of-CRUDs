<template>
  <v-layout justify-center>
    <v-flex xs12 sm12>
      <!-- INFORMAÇÕES DO PEDIDO -->
      <div class="white elevation-2">
        <v-toolbar flat dense class="red darken-3" dark>
          <v-toolbar-title> Informações do Pedido </v-toolbar-title>
        </v-toolbar>

        <v-container fluid grid-list-xl>
          <v-layout wrap align-center>
            <v-flex xs12 sm4 d-flex>
              <v-select v-model="order.factory" :items="factories" label="Fábrica"></v-select>
            </v-flex>
        
            <v-flex xs12 sm8 d-flex>
              <v-menu ref="menu" :close-on-content-click="true" v-model="menu" :nudge-right="40" :return-value.sync="date" lazy transition="scale-transition" offset-y full-width min-width="290px">
                <v-text-field slot="activator" v-model="order.expectedReceivedDate" label="Data de Entrega Esperada" prepend-icon="event"></v-text-field>
                <v-date-picker v-model="order.expectedReceivedDate" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn flat color="primary" @click="dateMenu = false">Cancelar</v-btn>
                  <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-flex>
          </v-layout>
        </v-container>
      </div>
      
      <br/>
      
      <!-- ITENS DO PEDIDO -->
      <div class="white elevation-2">
        <v-toolbar flat dense class="red darken-3" dark>
          <v-toolbar-title>Items do Pedido</v-toolbar-title>
          <v-spacer></v-spacer>

          <v-dialog v-model="dialog" max-width="500px">
            <v-btn slot="activator" outline dark class="red darken-3">Adicionar Item</v-btn>
            <v-card>
              <v-card-title>
                <span class="headline">Adicionar Item</span>
              </v-card-title>

              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                    <v-flex xs12 sm12>
                      <v-select v-bind:items="itemsToChoose" 
                                v-model="choosedItem" 
                                label="Nome" 
                                item-text="name" 
                                autocomplete 
                                return-object
                                required
                                @keyup.enter="addValueOnEnter" ></v-select>  
                    </v-flex>
                    <v-flex xs12 sm12>
                      <v-text-field readonly v-model="choosedItem.description" label="Descrição"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6>
                      <v-text-field readonly v-model="choosedItem.unitPrice" label="Preço Unitário"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6>
                      <v-text-field v-model="choosedItem.qty" 
                                    label="Quantidade" 
                                    required
                                    :rules="[() => choosedItem.qty > 0 || 'Quantidade maior que zero']"></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click.native="close">Cancelar</v-btn>
                <v-btn color="blue darken-1" flat @click.native="save" :disabled="!isValidQty || choosedItem.name === ''">Inserir</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>

        <v-data-table :headers="headers" :items="order.items" hide-actions class="elevation-1">
          <template slot="items" slot-scope="props">
            <td class="">{{ props.item.code }}</td>
            <td class="">{{ props.item.name }}</td>
            <td class="">{{ props.item.description }}</td>
            <td class="">{{ props.item.unitPrice }}</td>
            <td class="">{{ props.item.qty }}</td>
            <td class="justify-center layout px-0"> <v-icon small @click="deleteItem(props.item)" > delete </v-icon> </td>
          </template>
        </v-data-table>
      </div>

      <v-dialog v-model="orderSendDialog" width="500" 
                :disabled="order.items.length <= 0 || order.factory === ''">
        <v-btn slot="activator" outline 
               :disabled="order.items.length <= 0  || order.factory === ''"
               @click="sendOrder"> Enviar Pedido </v-btn>

        <v-card>
          <v-card-text> Pedido enviado! </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" flat @click="navigateTo({name: 'root'})"> Ok </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-flex>
  </v-layout>
</template>

<script>
  export default {
    data: () => ({
      order: {
        factory: '',
        expectedReceivedDate: null,
        items: []
      },
      
      validOrderMsg: '',
      isValidQty: false,
      dateMenu: null,
      date: null,
      menu: null,
      dialog: false,
      orderSendDialog: false,
      
      choosedItem: { 
        code: '',
        name: '',
        description: '',
        unitPrice: 0,
        qty: ''
      },      

      headers: [
        { text: 'Código', align: 'left', sortable: false, value: 'id', align: 'center' },
        { text: 'Nome', value: 'name', sortable: false, align: 'center' },
        { text: 'Descrição', value: 'description', sortable: false, align: 'center' },
        { text: 'Preço Unitário', value: 'unitPrice', sortable: false, align: 'center' },
        { text: 'Quantidade', value: 'qty', sortable: false, align: 'center' },
        { text: 'Ações', value: 'actions', sortable: false, align: 'center' }
      ],

      // TODO Catar isso das informações do usuário ou webservice
      itemsToChoose: [ { "code": 1, "name": "Chocolate - Pote Bola 150ml", "description": "Chocolate - Pote Bola 150ml", "unitPrice": 3.8 }, { "code": 2, "name": "Morango - Pote Bola 150ml", "description": "Morango - Pote Bola 150ml", "unitPrice": 3.8 }, { "code": 3, "name": "Chocolate - Pote Moreninha", "description": "Chocolate - Pote Moreninha", "unitPrice": 4.25 }, { "code": 4, "name": "Chocolate - Pote Moreninha", "description": "Chocolate - Pote Moreninha", "unitPrice": 4.25 }, { "code": 5, "name": "Chocolate - Pote Sundae 150ml", "description": "Chocolate - Pote Sundae 150ml", "unitPrice": 5 }, { "code": 6, "name": "Morango - Pote Sundae 150ml", "description": "Morango - Pote Sundae 150ml", "unitPrice": 5 }, { "code": 7, "name": "Flocos - Pote Sundae 150ml", "description": "Flocos - Pote Sundae 150ml", "unitPrice": 5 }, { "code": 8, "name": "Chocolate - Pote Moreninha", "description": "Chocolate - Pote Moreninha", "unitPrice": 5 }, { "code": 9, "name": "Creme - 500ml", "description": "Creme - 500ml", "unitPrice": 9 }, { "code": 10, "name": "Napolitano - 1 Litro", "description": "Napolitano - 1 Litro", "unitPrice": 10 }, { "code": 11, "name": "Nata com Avelã - 1 Litro", "description": "Nata com Avelã - 1 Litro", "unitPrice": 11 }, { "code": 12, "name": "Ninho Natti - 1 Litro", "description": "Ninho Natti - 1 Litro", "unitPrice": 11 }, { "code": 13, "name": "Iogurte com Amarena - 1 Litro", "description": "Iogurte com Amarena - 1 Litro", "unitPrice": 11 }, { "code": 14, "name": "Torta Alemã - 1 Litro", "description": "Torta Alemã - 1 Litro", "unitPrice": 11 }, { "code": 15, "name": "Ferrero Natti - 1 Litro", "description": "Ferrero Natti - 1 Litro", "unitPrice": 11 }, { "code": 16, "name": "Coco - 1 Litro", "description": "Coco - 1 Litro", "unitPrice": 11 }, { "code": 17, "name": "Morango - 1 Litro", "description": "Morango - 1 Litro", "unitPrice": 11 }, { "code": 18, "name": "Chocolate - 1 Litro", "description": "Chocolate - 1 Litro", "unitPrice": 11 }, { "code": 19, "name": "Creme - 1 Litro", "description": "Creme - 1 Litro", "unitPrice": 11 }, { "code": 20, "name": "Milho Verde - 1 Litro", "description": "Milho Verde - 1 Litro", "unitPrice": 11 }, { "code": 21, "name": "Abacaxi - 1 Litro", "description": "Abacaxi - 1 Litro", "unitPrice": 11 }, { "code": 22, "name": "Passas ao rum - 1 Litro", "description": "Passas ao rum - 1 Litro", "unitPrice": 11 }, { "code": 23, "name": "Chiclete - 1 Litro", "description": "Chiclete - 1 Litro", "unitPrice": 11 }, { "code": 24, "name": "Ferrero Natti - 1 Litro", "description": "Ferrero Natti - 1 Litro", "unitPrice": 11 }, { "code": 25, "name": "Iogurte com Amarena - 1 Litro", "description": "Iogurte com Amarena - 1 Litro", "unitPrice": 16 }, { "code": 26, "name": "Nata com Avelã - 1 Litro", "description": "Nata com Avelã - 1 Litro", "unitPrice": 16 }, { "code": 27, "name": "Ninho Natti - 1 Litro", "description": "Ninho Natti - 1 Litro", "unitPrice": 16 }, { "code": 28, "name": "Chocolate - 2 Litros", "description": "Chocolate - 2 Litros", "unitPrice": 21 }, { "code": 29, "name": "Chocolate e Morango - 2 Litros", "description": "Chocolate e Morango - 2 Litros", "unitPrice": 22 }, { "code": 30, "name": "Chocolate e Flocos - 2 Litros", "description": "Chocolate e Flocos - 2 Litros", "unitPrice": 22 }, { "code": 31, "name": "Creme Crocante e Nata - 2 Litros", "description": "Creme Crocante e Nata - 2 Litros", "unitPrice": 22 }, { "code": 32, "name": "Napolitano - 2 Litros", "description": "Napolitano - 2 Litros", "unitPrice": 22 }, { "code": 33, "name": "Passas ao Rum e Flocos - 2 Litros", "description": "Passas ao Rum e Flocos - 2 Litros", "unitPrice": 22 }, { "code": 34, "name": "Limão e Uva - 2 Litros", "description": "Limão e Uva - 2 Litros", "unitPrice": 22 }, { "code": 35, "name": "Flocos - 2 Litros", "description": "Flocos - 2 Litros", "unitPrice": 22 }, { "code": 36, "name": "Creme e Morango - 2 Litros", "description": "Creme e Morango - 2 Litros", "unitPrice": 22 }, { "code": 37, "name": "Ferrero Natti - 2 Litros", "description": "Ferrero Natti - 2 Litros", "unitPrice": 24 }, { "code": 38, "name": "Torta Alemã - 2 Litros", "description": "Torta Alemã - 2 Litros", "unitPrice": 24 }, { "code": 39, "name": "Kinder Natti - 2 Litros", "description": "Kinder Natti - 2 Litros", "unitPrice": 24 }, { "code": 40, "name": "Trufa Natti - 2 Litros", "description": "Trufa Natti - 2 Litros", "unitPrice": 24 }, { "code": 41, "name": "Clássico - Sensonatti", "description": "Clássico - Sensonatti", "unitPrice": 5 }, { "code": 42, "name": "Clássico - Skimonatti", "description": "Clássico - Skimonatti", "unitPrice": 5 }, { "code": 43, "name": "Conatti - Baunilha", "description": "Conatti - Baunilha", "unitPrice": 6 }, { "code": 44, "name": "Conatti - Chocoflair", "description": "Conatti - Chocoflair", "unitPrice": 6 }, { "code": 45, "name": "Conatti - Torta Alemã", "description": "Conatti - Torta Alemã", "unitPrice": 6 }, { "code": 46, "name": "Cremosos - Chocolate", "description": "Cremosos - Chocolate", "unitPrice": 3.5 }, { "code": 47, "name": "Cremosos - Coco", "description": "Cremosos - Coco", "unitPrice": 3.5 }, { "code": 48, "name": "Cremosos - Milho Verde", "description": "Cremosos - Milho Verde", "unitPrice": 3.5 }, { "code": 49, "name": "Cremosos - Morango", "description": "Cremosos - Morango", "unitPrice": 3.5 }, { "code": 50, "name": "Frutanatti - Abacaxi", "description": "Frutanatti - Abacaxi", "unitPrice": 3.5 }, { "code": 51, "name": "Frutanatti - Limão", "description": "Frutanatti - Limão", "unitPrice": 3.5 }, { "code": 52, "name": "Frutanatti - Maracujá", "description": "Frutanatti - Maracujá", "unitPrice": 3.5 }, { "code": 53, "name": "Frutanatti - Uva", "description": "Frutanatti - Uva", "unitPrice": 3.5 }, { "code": 54, "name": "Kids - Pinta Língua", "description": "Kids - Pinta Língua", "unitPrice": 1.5 }, { "code": 55, "name": "Kids - Tutti Frutti", "description": "Kids - Tutti Frutti", "unitPrice": 1.5 }, { "code": 56, "name": "Meganatti - Chocolate Branco", "description": "Meganatti - Chocolate Branco", "unitPrice": 7 }, { "code": 57, "name": "Meganatti - Chocolate Suiço", "description": "Meganatti - Chocolate Suiço", "unitPrice": 7 }, { "code": 58, "name": "Meganatti - Original", "description": "Meganatti - Original", "unitPrice": 7 }, { "code": 59, "name": "Supremo - Brigadeiro", "description": "Supremo - Brigadeiro", "unitPrice": 4.5 }, { "code": 60, "name": "Supremo - Chocolate Branco", "description": "Supremo - Chocolate Branco", "unitPrice": 4.5 }, { "code": 61, "name": "Supremo - Fascínio", "description": "Supremo - Fascínio", "unitPrice": 4.5 }, { "code": 62, "name": "Supremo - Flokito", "description": "Supremo - Flokito", "unitPrice": 4.5 }, { "code": 63, "name": "Paleta Mexicana - Ninho trufado", "description": "Paleta Mexicana - Ninho trufado", "unitPrice": 8.5 }, { "code": 64, "name": "Paleta Mexicana - Iogurte com amora", "description": "Paleta Mexicana - Iogurte com amora", "unitPrice": 8.5 }, { "code": 65, "name": "Paleta Mexicana - Iogurte com amora", "description": "Paleta Mexicana - Iogurte com amora", "unitPrice": 8.5 } ],
      factories: ['Bonatti Indaial', 'Fábrica 2'],
    }),

    watch: {
      dialog (val) {
        val || this.close()
      },

      'choosedItem.qty' () {
        if (this.choosedItem.qty > 0) {
          this.isValidQty = true
        } else {
          this.isValidQty = false
        }
      },

    },

    methods: {
      addValueOnEnter (e) {
        let selectedItem = this.itemsToChoose.find((obj) => { return obj.name === this.choosedItem.name })
        this.choosedItem = selectedItem
      },

      deleteItem (item) {
        const index = this.order.items.indexOf(item)
        confirm('Deseja remover o item?') && this.order.items.splice(index, 1)
      },

      close () {
        this.dialog = false
        setTimeout(() => {
          this.choosedItem = {}
        }, 300)
      },

      save () {
        this.order.items.push(this.choosedItem)
        this.close()
      },

      sendOrder () {
        // TODO: fazer post do pedido
        console.log(this.order)
      },

      navigateTo (route) {
        this.$router.push(route)
      }


    }
  }
</script>
