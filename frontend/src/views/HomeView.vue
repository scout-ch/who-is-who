<script setup>
import { ref } from 'vue'
import axios from 'axios'

import ConfigInput from '@/components/widgets/ConfigInput.vue'
import Groups from '@/components/group/Groups.vue'
import Generator from '@/components/Generator.vue'
import Loading from '@/components/widgets/Loader.vue'

import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'

const dataStore = useDataStore()
const configStore = useConfigStore()

const loadConfig = axios.get('/api/config')
const loadData = axios.get('/api')
console.log(loadConfig)
console.log(loadData)

const loading = ref(true)
const loadError = ref(false)

Promise.all([loadData, loadConfig])
  .then(([resData, resConfig]) => {
    // Initialize data store
    const data = resData.data
    dataStore.initialize(data)

    // Initialize config store
    const config = resConfig.data
    configStore.initialize(config)

    loading.value = false
    loadError.value = false
  })
  .catch((err) => {
    console.error('Error initializing data: ', err)
    loading.value = false
    loadError.value = true
  })
</script>

<template>
  <main class="h-full m-auto">
    <Loading v-if="loading" class="mt-30" />
    <div v-else>
      <div
        v-if="loadError"
        class="text-lg text-center border m-5 p-5 bg-rose-200 text-rose-950 border-rose-400 rounded-2xl"
      >
        Loading failed.
      </div>
      <div v-else class="flex justify-center gap-3 w-5/6 m-auto mt-1">
        <Groups class="w-full min-w-2xl" />
        <Generator class="w-full" />
      </div>
    </div>
  </main>
</template>
