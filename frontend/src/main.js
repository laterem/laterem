import { createApp } from "vue";
import App from "./App.vue";
import HeaderApp from "./HeaderApp.vue";
// import NavTreeApp from "./App.vue";
import router from "./router";

createApp(App).use(router).mount("#app");
createApp(HeaderApp).mount("#header");
// createApp(NavTreeApp).mount("#nav-tree");
