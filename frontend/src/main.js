import { createApp } from "vue";
import App from "./App.vue";
import HeaderApp from "./HeaderApp.vue";
// import NavTreeApp from "./App.vue";
import router from "./router";
import VueSession from "./vue-session";

createApp(App).use(VueSession).use(router).mount("#app");
createApp(HeaderApp).use(VueSession).use(router).mount("#header");
