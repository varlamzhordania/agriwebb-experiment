<script setup>

import {oAuth2Install} from "../lib/api/authorization.js";
import {useRoute} from "vue-router"
import {onMounted, ref} from "vue";

const route = useRoute()

const LoggedIn = ref(false)

onMounted(() => {
  const {authorization} = route.query

  if (authorization && authorization === "successful") {
    LoggedIn.value = true
  }
})

const handleLogin = () => {
  const url = oAuth2Install()
  return location.href = url
}


</script>
<template>
  <div class="container h-dvh flex justify-center items-center">
    <div class="bg-white shadow rounded p-4">
      <h2 class="text-5xl font-bold text-zinc-600">Login</h2>
      <p class="text-base text-zinc-500 my-2">Start authorization flow on AgriWebb</p>

      <div v-if="LoggedIn">
        <h3 class="text-xl text-green-600">You are successfully logged in!</h3>
      </div>

      <button class="btn-primary w-full" @click="handleLogin" v-if="!LoggedIn">
        Start Authorization
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>