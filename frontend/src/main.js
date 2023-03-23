import { createApp } from 'vue'
import App from './App.vue'
import NavTreeApp from './NavTreeApp.vue'

const app = createApp(App);
app.mount('#app');

const navTree = createApp(NavTreeApp);
navTree.mount('#nav-tree');
