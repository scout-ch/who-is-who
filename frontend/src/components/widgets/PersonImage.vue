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

const reset = () => {
  if (props.person_id in configStore.images) {
    delete configStore.images[props.person_id]
  }
  setImage()
}

const setImage = () => {
  if (props.person_id in configStore.images) {
    imageUrl.value = `/api/image/${configStore.images[props.person_id]}`
  } else {
    imageUrl.value = dataStore.images[props.person_id]
  }
}

onMounted(() => {
  setImage()
})
</script>

<template>
  <div>
    <img :src="imageUrl" alt="Person Image" class="min-w-30 max-h-30 rounded-b-xl object-cover" />
    <span class="flex w-full h-2/7 justify-between pl-3 pr-2 pb-2">
      <v-icon
        name="bi-upload"
        class="cursor-pointer w-auto h-auto hover:bg-gray-100"
        @click="triggerFileInput"
      />
      <v-icon
        name="la-undo-alt-solid"
        class="cursor-pointer w-auto h-auto hover:bg-gray-100"
        @click="reset()"
      />
    </span>

    <input
      type="file"
      ref="fileInput"
      accept="image/*"
      @change="handleFileChange"
      style="display: none"
    />
  </div>
</template>
