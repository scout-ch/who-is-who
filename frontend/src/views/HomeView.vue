<script setup>
import { ref } from 'vue'
import axios from 'axios'

import Groups from '@/components/group/Groups.vue'
import Generator from '@/components/Generator.vue'
import Loading from '@/components/widgets/Loader.vue'

import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'

const dataStore = useDataStore()
const configStore = useConfigStore()

const loadConfig = axios.get('/api/config')
const loadData = axios.get('/api')

const loading = ref(true)
Promise.all([loadData, loadConfig])
  .then(([resData, resConfig]) => {
    // Initialize data store
    const data = resData.data
    dataStore.initialize(data)

    // Initialize config store
    const config = resConfig.data
    configStore.initialize(config)

    loading.value = false
  })
  .catch((err) => {
    console.error('Error initializing data: ', err)
  })
</script>

<template>
  <main class="h-full m-auto">
    <Loading v-if="loading" class="mt-30" />
    <div v-else class="flex justify-center gap-3 w-5/6 m-auto mt-1">
      <Groups class="w-full min-w-2xl" />
      <Generator class="w-full" />
    </div>
  </main>
</template>
