<script setup>
import { useConfigStore } from '@/stores/configStore'
import { ref } from 'vue'
const configStore = useConfigStore()

const showConfigString = ref(false)
const configString = ref('')
const copiedToClipboard = ref(false)
const invalidConfigString = ref(false)

function configReset() {
  configStore.reset()
  configStore.postConfig().then((_) => {
    window.location.reload()
  })
}
function configShow() {
  showConfigString.value = true
  configString.value = configStore.getString()
}
function getConfigStringInput() {
  return document.getElementById('configStringInput').textContent
}
async function configCopy() {
  const type = 'text/plain'
  const config = getConfigStringInput()
  const clipboardItemData = {
    [type]: config,
  }
  const clipboardItem = new ClipboardItem(clipboardItemData)
  await navigator.clipboard.write([clipboardItem])
  copiedToClipboard.value = true
}
function configUpdate() {
  const config = getConfigStringInput()
  try {
    configStore.fromString(config)
    configStore.postConfig().then((_) => {
      window.location.reload()
    })
  } catch {
    invalidConfigString.value = true
  }
}
function configCancel() {
  showConfigString.value = false
  copiedToClipboard.value = false
  invalidConfigString.value = false
}
</script>
<template>
  <div class="border border-amber-600 rounded-2xl max-w-full">
    <div v-if="showConfigString">
      <div class="flex align-middle p-2">
        <p class="pt-2">String:</p>
        <div
          id="configStringInput"
          contenteditable
          class="ml-2 w-full h-full border rounded-sm resize-y break-all p-1 hover:bg-gray-100"
          :textContent="configString"
        />
      </div>
      <div class="flex justify-between">
        <p
          class="cursor-pointer h-full ml-15 m-2 text-red-900 border justify-self-start p-1 border-red-900 rounded-md hover:bg-red-900/50"
          @click="configReset()"
        >
          Reset <v-icon name="la-undo-alt-solid" class="w-auto h-auto ml-1" />
        </p>
        <div class="flex gap-2 justify-end p-2">
          <p
            class="cursor-pointer text-amber-500 border p-1 border-amber-500 rounded-md hover:bg-amber-300/50"
            @click="configCopy()"
          >
            Copy <v-icon name="la-copy" class="w-auto h-auto ml-1" />
          </p>
          <p
            class="cursor-pointer text-green-500 border p-1 border-green-500 rounded-md hover:bg-teal-300/50"
            @click="configUpdate()"
          >
            Set
            <v-icon name="bi-upload" class="w-auto h-auto ml-1" />
          </p>
          <p
            class="cursor-pointer text-red-500 border p-1 border-red-500 rounded-md hover:bg-red-300/50"
            @click="configCancel()"
          >
            Cancel
          </p>
        </div>
      </div>
    </div>
    <div
      v-else
      class="cursor-pointer h-full w-full p-2 rounded-2xl text-xl hover:bg-amber-100/50"
      @click="configShow()"
    >
      Configuration Options
    </div>
  </div>

  <div v-show="copiedToClipboard" class="bg-gray-100">
    Copied configuration string to clipboard.
  </div>
  <div v-show="invalidConfigString" class="bg-red-100">Invalid Config String, can't parse</div>
</template>
