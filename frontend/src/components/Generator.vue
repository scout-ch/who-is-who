<script setup>
import { ref, useTemplateRef, onMounted } from 'vue'
import axios from 'axios'
import { PlayIcon, ArrowDownIcon } from '@heroicons/vue/24/outline'

import { useConfigStore } from '@/stores/configStore'
const configStore = useConfigStore()

const loading = ref(true)
const preview = useTemplateRef('preview')

const root_group_url = '/api/html/de/2'

function initialPreview() {
  axios
    .get(root_group_url)
    .then((_res) => {
      preview.value.src = root_group_url
    })
    .catch((err) => {
      console.log(`Server not ready or site not generated: ${err}`)
    })
}

function fetchHtml() {
  loading.value = true
  axios
    .get('/api/render')
    .then((_res) => {
      loading.value = false
      preview.value.src = root_group_url
    })
    .catch(function (err) {
      console.error('Failed to render:', err)
    })
}

function postConfig() {
  axios
    .post('/api/config', {
      data: configStore.theState(),
    })
    .catch((err) => {
      console.error('Failed to post config:', err)
    })
}

function generate() {
  postConfig()
  fetchHtml()
}

function downloadZip() {
  postConfig()
  axios
    .get('/api/download-zip', { responseType: 'blob' })
    .then((res) => {
      const fileUrl = window.URL.createObjectURL(res.data)
      const fileName = res.headers['content-disposition'].match(/filename=(.+)/)[1]
      const link = document.createElement('a')
      link.href = fileUrl
      link.download = fileName

      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(fileUrl)
    })
    .catch((err) => {
      console.log(`Download failed: ${err}`)
    })
}

onMounted(() => {
  initialPreview()
})
</script>

<template>
  <div>
    <span class="flex items-center justify-between w-full">
      <a href="#" @click.prevent="generate">
        <span class="flex align-middle justify-center">
          <p class="w-full h-full mt-1">Generate preview</p>
          <PlayIcon class="w-7 pt-1 justify-start cursor-pointer" />
        </span>
      </a>
      <a href="#" @click.prevent="downloadZip">
        <span class="flex align-middle justify-center">
          <p class="w-full h-full mt-1">Download</p>
          <ArrowDownIcon class="w-7 pt-1 justify-end cursor-pointer" />
        </span>
      </a>
    </span>
    <div class="">
      <iframe
        ref="preview"
        class="w-full max-w-1/1 resize overflow-auto border rounded-lg m-0"
        height="700"
        :src=""
      />
    </div>
  </div>
</template>
