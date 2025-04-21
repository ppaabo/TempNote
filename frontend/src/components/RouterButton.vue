<!-- Simple, reusable button that can be used with Vue Router -->
<script setup>
import { useRouter } from "vue-router";
/**
 * @prop {String|Object} to - The route to navigate to. Can be either a string (route name) or an object (route definition).
 * @prop {String} [text="Button"] - The text to display on the button. Defaults to "Button". Can also be passed as a slot.
 * @prop {String} [btnClass="btn btn-secondary"] - The CSS class for the button. Defaults to "btn btn-secondary".
 */
const props = defineProps({
  to: {
    type: [String, Object],
    required: true,
  },
  text: {
    type: String,
    default: "Button",
  },
  btnClass: {
    type: String,
    default: "btn btn-secondary",
  },
});

const router = useRouter();

const navigate = () => {
  if (typeof props.to === "string") {
    router.push({ name: props.to });
  } else {
    router.push(props.to);
  }
};
</script>
<template>
  <button :class="btnClass" @click="navigate">
    <slot>{{ text }}</slot>
  </button>
</template>
<style scoped></style>
