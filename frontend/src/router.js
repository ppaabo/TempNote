import { createWebHistory, createRouter } from "vue-router";

import MessageComposer from "./components/MessageComposer.vue";
import MessageReader from "./components/MessageReader.vue";
import MessageSaved from "./components/MessageSaved.vue";

const routes = [
  { path: "/", name: "write", component: MessageComposer },
  { path: "/saved/:id", name: "save", component: MessageSaved, props: true },
  { path: "/read/:id", name: "read", component: MessageReader, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
