<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { PlayIcon, CloudArrowUpIcon } from '@heroicons/vue/24/outline'

import Loading from '@/components/widgets/Loader.vue'
import { useConfigStore } from '@/stores/configStore'
const configStore = useConfigStore()

const loading = ref(true)
const server_ready = ref(false)

const locales = ['de', 'fr', 'it']

const preview_root = '/api/preview/'
let locale = ref('de')
let preview = ref(preview_root + locale.value)

function initialPreview() {
  axios
    .get(preview)
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
      server_ready.value = true
    })
    .catch(function (err) {
      console.error('Failed to render:', err)
    })
}

function generate() {
  configStore.postConfig().then((_) => {
    generateHtml()
  })
}

function upload() {
  axios.get('/api/publish').catch(function (err) {
    console.error('Failed to render:', err)
  })
}

function changeLocale(loc) {
  locale.value = loc
  refreshPreview()
}

function refreshPreview() {
  preview.value = preview_root + locale.value
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
          <p class="w-full h-full mt-1">Generate</p>
          <PlayIcon class="w-7 pt-1 justify-start cursor-pointer" />
        </span>
      </a>
      <span class="flex align-middle" >
        <div v-for="locale in locales" class="p-1 pt-4">
          <span class="flex align-middle justify-center  cursor-pointer" @click.prevent="changeLocale(locale)">
            <v-icon :name="'fi-' + locale" squared="false" />
          </span>
        </div>
      </span>
      <a href="#" @click.prevent="upload">
        <span class="flex align-middle justify-center pt-2">
          <p class="w-full h-full mt-1">Upload</p>
          <CloudArrowUpIcon class="w-7 pt-1 justify-start cursor-pointer" />
        </span>
      </a>
    </span>
    <Loading v-if="loading" class="mt-10" />
    <div v-else>
      <div v-if="server_ready">
        <iframe
          class="w-full max-w-1/1 resize overflow-auto border rounded-lg m-0"
          height="1200"
          :src="preview"
        />
      </div>
      <div
        v-else
        class="text-lg border m-5 p-5 w-1/2 bg-rose-200 text-rose-950 border-rose-400 rounded-2xl"
      >
        Loading preview failed<br />
      </div>
    </div>
  </div>
</template>
