<script setup>
import { ref, onMounted } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'
import axios from 'axios'

const props = defineProps({
  person_id: { type: String },
})

const imageUrl = ref(null)
const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const defaultImage = '/favicon.png'

const configStore = useConfigStore()
const dataStore = useDataStore()

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
    uploadImage(file)
  }
}

const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('image', file)

  axios
    .post(`/api/image-upload/${props.person_id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then((res) => {
      const filename = res.data.filename
      imageUrl.value = `/api/image/${filename}`
      configStore.images[props.person_id] = filename
    })
    .catch((err) => {
      console.error(err)
    })
}

onMounted(() => {
  if (props.person_id in configStore.images) {
    imageUrl.value = `/api/image/${configStore.images[props.person_id]}`
  } else {
    imageUrl.value = dataStore.images[props.person_id]
  }
})
</script>

<template>
  <div>
    <img
      :src="imageUrl"
      alt="Click to upload"
      @click="triggerFileInput"
      class="cursor-pointer min-w-25 max-h-25 border rounded-lg object-cover mr-2"
    />
    <input
      type="file"
      ref="fileInput"
      accept="image/*"
      @change="handleFileChange"
      style="display: none"
    />
  </div>
</template>
