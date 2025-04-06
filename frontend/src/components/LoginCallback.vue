<script setup>
import {onMounted} from 'vue'
import {useRoute} from 'vue-router'
import {useRouter} from 'vue-router'
import {BASE_URL} from "../config.js";
import {exchangeAuthorizationCode} from "../lib/api/authorization.js";

const route = useRoute()
const router = useRouter()

onMounted(() => {
  const {code, error, error_description, state} = route.query

  if (code) {
    handleAuthorizationCode(code, state)
  } else if (error) {
    handleAuthorizationError(error, error_description)
  }
})

const handleAuthorizationCode = (code, state) => {
  console.log("Authorization code:", code)
  console.log("State parameter:", state)

  const redirectUri = `${BASE_URL}/?authorization=success`;

  exchangeAuthorizationCode(code, redirectUri)
      .then(tokenData => {
        console.log('Received Token Data:', tokenData);
      })
      .catch(error => {
        console.error('Error:', error);
      });
}

const handleAuthorizationError = (error, error_description) => {
  console.error("Error during authorization:", error)
  console.error("Error description:", error_description)
  router.push('/')
}
</script>

<template>
  <div class="container">
    <h2>Authorization Callback</h2>
    <p>Processing your authorization...</p>
  </div>
</template>
