<script setup>
import { ref } from 'vue'
import axios from 'axios'

import ConfigInput from '@/components/widgets/ConfigInput.vue'
import Groups from '@/components/group/Groups.vue'
import Generator from '@/components/Generator.vue'
import Loading from '@/components/widgets/Loader.vue'
import Configuration from '@/components/Configuration.vue'

import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'

const dataStore = useDataStore()
const configStore = useConfigStore()

const loading = ref(true)
const loadError = ref(false)

async function init() {
  try {
    const [resData, resConfig] = await Promise.all([
      axios.get('/api'),
      axios.get('/api/config'),
    ])

    // Do the risky work before touching any store, or make initialize() atomic
    dataStore.initialize(resData.data)
    configStore.initialize(resConfig.data)

    loadError.value = false
  } catch (err) {
    console.error('Error initializing data:', err)
    loadError.value = true
  } finally {
    loading.value = false
  }
}

init()

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
        <div class="w-full">
          <Groups class="w-full min-w-2xl" />
          <Configuration />
        </div>
        <Generator class="w-full" />
      </div>
    </div>
  </main>
</template>
