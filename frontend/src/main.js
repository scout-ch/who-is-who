import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { FiDe, FiIt, FiFr, RiArrowGoBackLine, LaUndoAltSolid } from 'oh-vue-icons/icons'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia)

addIcons(FiDe, FiIt, FiFr, RiArrowGoBackLine, LaUndoAltSolid)
app.component('v-icon', OhVueIcon)

app.mount('#app')
