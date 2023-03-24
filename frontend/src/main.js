import { createApp } from "vue";
import App from "./App.vue";
import NavTreeApp from "./NavTreeApp.vue";
import router from "./router";

createApp(App).use(router).mount("#app");
createApp(NavTreeApp).use(router).mount("#nav-tree");
