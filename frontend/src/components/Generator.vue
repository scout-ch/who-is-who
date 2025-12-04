<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { PlayIcon, ArrowDownIcon } from '@heroicons/vue/24/outline'

import Loading from '@/components/widgets/Loader.vue'
import { useConfigStore } from '@/stores/configStore'
const configStore = useConfigStore()

const loading = ref(true)
const server_ready = ref(false)

const root_group_url = '/api/full_html/de/2'

function initialPreview() {
  axios
    .get(root_group_url)
    .then((_res) => {
      loading.value = false
      server_ready.value = true
    })
    .catch((_err) => {
      loading.value = false
      server_ready.value = false
    })
}

function generateHtml() {
  loading.value = true
  axios
    .get('/api/render', { timeout: 180000 })
    .then((_res) => {
      loading.value = false
    })
    .catch(function (err) {
      console.error('Failed to render:', err)
    })
}

function generate() {
  configStore.postConfig()
  setTimeout(generateHtml, 150)
}

onMounted(() => {
  initialPreview()
})
</script>

<template>
  <div>
    <span class="flex items-center justify-between w-full">
      <a href="#" @click.prevent="generate">
        <span class="flex align-middle justify-center pt-2">
          <p class="w-full h-full mt-1">Generate preview</p>
          <PlayIcon class="w-7 pt-1 justify-start cursor-pointer" />
        </span>
      </a>
    </span>
    <Loading v-if="loading" class="mt-10" />
    <div v-else>
      <div v-if="server_ready">
        <iframe
          class="w-full max-w-1/1 resize overflow-auto border rounded-lg m-0"
          height="1200"
          :src="root_group_url"
        />
      </div>
      <div
        v-else
        class="text-lg border m-5 p-5 w-1/2 bg-rose-200 text-rose-950 border-rose-400 rounded-2xl"
      >
        Loading preview failed.<br />
        Has the site been generated and is the server ready?
      </div>
    </div>
  </div>
</template>
