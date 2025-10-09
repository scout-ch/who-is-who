<script setup>
import { useTemplateRef } from 'vue'

const props = defineProps({
  id: {
    type: String,
  },
  configField: {
    type: Object,
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
})

const cinput = useTemplateRef('cinput')

function setConfig(text) {
  props.configField[id] = text
}

function reset() {
  delete props.configField[id]
}
</script>

<template>
  <span class="flex gap-2 m-1 items-center">
    <div class="text-lg">{{ props.label }}:</div>
    <div
      :ref="cinput"
      contenteditable="true"
      class="w-full border rounded-sm resize-none h-10 p-1 items-center text-lg flex hover:bg-gray-100"
      @keyup="setConfig($event.target.textContent, locale)"
      @keyup.enter.exact="$event.target.blur()"
      :placeholder="props.placeholder"
    ></div>
    <v-icon name="la-undo-alt-solid" @click="reset()" class="cursor-pointer" />
  </span>
</template>
