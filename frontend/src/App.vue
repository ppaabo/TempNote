<script setup>
import MessageComposer from "./components/MessageComposer.vue";
import MessageReader from "./components/MessageReader.vue";
</script>

<template>
  <div class="app-container">
    <MessageComposer />
    <MessageReader />
  </div>
</template>

<style scoped>
.app-container {
  width: 70vh;
  display: flex;
  flex-direction: column;
}
</style>
