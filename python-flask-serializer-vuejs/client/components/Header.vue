<template>
    <v-toolbar fixed class="red darken-3" dark>
        <v-toolbar-title class="mr-4" >
            <span class="home" @click="navigateTo({name: 'root'})"> Bonatti Web </span>
        </v-toolbar-title>

        <v-toolbar-items>
            <v-btn flat dark @click="navigateTo({name: 'root'})"> Início </v-btn>
        </v-toolbar-items>

        <v-toolbar-items>
            <v-btn v-if="$store.state.isUserLoggedIn" flat dark @click="navigateTo({name: 'orders'})"> Pedidos </v-btn>
        </v-toolbar-items>

        <v-toolbar-items>
            <v-btn v-if="$store.state.isUserLoggedIn" flat dark @click="navigateTo({name: 'sales'})"> Vendas </v-btn>
        </v-toolbar-items>

        <v-spacer></v-spacer>

        <v-toolbar-items>
            <v-btn v-if="!$store.state.isUserLoggedIn" flat dark @click="navigateTo({name: 'login'})"> Login </v-btn>
        </v-toolbar-items>

        <v-toolbar-items>
            <v-btn v-if="$store.state.isUserLoggedIn" flat dark @click="logout"> Sair </v-btn>
        </v-toolbar-items>

        <v-toolbar-items>
            <v-btn v-if="!$store.state.isUserLoggedIn" flat dark @click="navigateTo({name: 'register'})"> Criar Conta </v-btn>
        </v-toolbar-items>

    </v-toolbar>
</template>

<script>
export default {
    methods: {
        navigateTo (route) {
            this.$router.push(route)
        },
        logout () {
            this.$store.dispatch('setToken', null)
            this.$store.dispatch('setUser', null)
            this.$router.push({ name: 'root' })
        }
    }
}
</script>

<style>
.home {
    cursor: pointer;
}

.home:hover {
    color: whitesmoke;
}
</style>
