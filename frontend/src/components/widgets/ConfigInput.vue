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
})

const cinput = useTemplateRef('cinput')

function setInput(text) {
  props.configField[props.id] = text
}

function getInput() {
  if (props.id in props.configField) {
    return props.configField[props.id]
  }
  return ''
}

function reset() {
  delete props.configField[props.id]
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
