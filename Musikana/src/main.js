import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // <--- Router importieren

const app = createApp(App);

app.use(router); // <--- Den Router der App hinzufügen

app.mount("#app");
