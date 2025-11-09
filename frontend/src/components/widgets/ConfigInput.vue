<script setup>
import { useTemplateRef } from 'vue'

import { useConfigStore } from '@/stores/configStore'

const props = defineProps({
  id: {
    type: String,
  },
  configFieldName: {
    type: String,
  },
  label: {
    type: String,
    default: '',
  },
})
const configStore = useConfigStore()

const configField = configStore.getField(props.configFieldName)
const cinput = useTemplateRef('cinput')

function setInput(text) {
  configField[props.id] = text
}

function getInput() {
  if (props.id in configField) {
    return configField[props.id]
  }
  return ''
}

function reset() {
  delete configField[props.id]
  cinput.value.textContent = ''
}
</script>

<template>
  <span class="flex gap-2 m-1 items-center">
    <div class="text-lg">{{ props.label }}:</div>
    <div class="w-full h-10 items-center text-lg flex">
      &nbsp;
      <div
        contenteditable
        class="w-full h-full border rounded-sm whitespace-nowrap resize-none p-1 hover:bg-gray-100"
        ref="cinput"
        @blur="setInput($event.target.textContent)"
        @keyup.enter.exact.prevent="$event.target.blur()"
      >
        {{ getInput() }}
      </div>
    </div>
    <v-icon name="la-undo-alt-solid" @click="reset()" class="cursor-pointer" />
  </span>
</template>
