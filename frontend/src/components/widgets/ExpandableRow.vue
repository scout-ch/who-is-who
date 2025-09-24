<script setup>
import { ref } from 'vue'
import { ChevronDownIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'

const expanded = ref(false)

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <span
    class="flex items-start w-full select-none cursor-pointer hover:bg-gray-100 rounded-lg"
    @click="expanded = !expanded"
  >
    <ChevronDownIcon v-if="expanded" class="mt-1.5 w-4 mr-2 cursor-pointer" />
    <ChevronRightIcon v-else class="mt-2 w-4 mr-2 cursor-pointer" />
    <div class="text-xl">{{ props.title }}</div>
  </span>
  <div v-show="expanded">
    <slot></slot>
  </div>
</template>
