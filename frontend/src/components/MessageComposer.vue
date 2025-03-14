<script setup>
import { ref } from "vue";
import { useCrypto } from "../composables/useCrypto.js";

const { encryptMsg } = useCrypto();

const message = ref("Secret Message");
const password = ref("super-secure-password");
const encrypted = ref(null);

const encrypt = async () => {
  encrypted.value = await encryptMsg(message.value, password.value);
};
</script>

<template>
  <div class="composer-container">
    <input class="text-input" v-model="message" placeholder="Enter message" />
    <input
      class="text-input"
      type="password"
      v-model="password"
      placeholder="Enter password"
    />
    <button class="button" @click="encrypt">Encrypt</button>
    <pre>{{ encrypted }}</pre>
  </div>
</template>

<style scoped>
.composer-container {
  display: flex;
  flex-direction: column;
}

input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
</style>
