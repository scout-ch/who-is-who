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

const loadData = axios.get('/api')
const loadConfig = axios.get('/api/config')

Promise.allSettled([loadData, loadConfig])
  .then(([resData, resConfig]) => {
    try {
      dataStore.initialize(resData.value.data)
    } catch (err){
      loadError.value = true
      console.log("Could not load data: ", err)
    }

    try {
      configStore.initialize(resConfig.value.data)
    } catch (err){
      loadError.value = true
      console.error("Could not load config: ", err)
    }

    loading.value = false
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
        <div class="w-full">
          <Groups class="w-full min-w-2xl" />
          <Configuration />
        </div>
        <Generator class="w-full" />
      </div>
    </div>
  </main>
</template>
