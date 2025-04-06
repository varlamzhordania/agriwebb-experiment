<script setup>

import {oAuth2Install} from "../lib/api/authorization.js";

const handleLogin = () => {
  const url = oAuth2Install()
  return location.href = url
}


</script>
<template>
  <div class="container h-dvh flex justify-center items-center">
    <div class="bg-white shadow rounded p-4">
      <h2 class="text-5xl font-bold text-zinc-600">Login</h2>
      <p class="text-base text-zinc-500 my-2">start authorization flow on agriwebb</p>
      <button class="btn-primary w-full" @click="handleLogin">
        Start Authorization
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>