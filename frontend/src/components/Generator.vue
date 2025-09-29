<script setup>
import { ref, useTemplateRef } from 'vue'
import axios from 'axios'
import { PlayIcon, ArrowDownIcon } from '@heroicons/vue/24/outline'

import { useConfigStore } from '@/stores/configStore'
const configStore = useConfigStore()

const preview = useTemplateRef('preview')
const loading = ref(true)

function fetchHtml() {
  loading.value = true
  axios
    .get('/api/render')
    .then((response) => {
      loading.value = false
      preview.value.src = preview.value.src
    })
    .catch(function (err) {})
}

function generate() {
  axios
    .post('/api/config', {
      data: configStore.theState(),
    })
    .then((res) => {
      fetchHtml()
    })
}
</script>

<template>
  <div>
    <span class="flex items-center justify-between w-full">
      <a href="#" @click.prevent="generate">
        <PlayIcon class="w-7 pt-1 justify-start cursor-pointer" />
      </a>
      <a href="/api/download-zip">
        <ArrowDownIcon class="w-7 pt-1 justify-end cursor-pointer" />
      </a>
    </span>
    <div class="">
      <iframe
        ref="preview"
        class="w-full max-w-1/1 resize overflow-auto border rounded-lg m-0"
        height="700"
        src="/api/static/de/2.html"
      />
    </div>
  </div>
</template>
