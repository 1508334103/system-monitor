import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Loading, Notify } from 'quasar'

// 导入 Quasar 的 CSS
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'  // 使用 .sass 扩展名

import App from './App.vue'

const app = createApp(App)

// 创建并使用 Pinia（状态管理）
app.use(createPinia())

// 配置 Quasar
app.use(Quasar, {
    plugins: {
        Loading,
        Notify
    },
    config: {
        // 可以在这里配置 Quasar 的默认值
        loading: {},
        notify: {}
    }
})

app.mount('#app')