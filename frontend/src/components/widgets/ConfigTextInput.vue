<script setup>
import { useTemplateRef, computed } from 'vue'

import { useConfigStore } from '@/stores/configStore'
const locales = ['de', 'fr', 'it']

const props = defineProps({
  id: {
    type: String,
  },
  configFieldName: {
    type: String,
  },
  defaultValues: {
    type: Object,
    default: {},
  },
})

const configStore = useConfigStore()

const configField = configStore.getField(props.configFieldName)
const initialValues = computed(() => {
  if (props.id in configField) {
    return { de: '', fr: '', it: '', ...props.defaultValues, ...configField[props.id] }
  }
  return { de: '', fr: '', it: '', ...props.defaultValues }
})

let inputRefs = {}
locales.forEach((loc) => {
  inputRefs[loc] = useTemplateRef(idByLocale(loc))
})

function idByLocale(locale) {
  return `cti-${locale}`
}

function setConfigText(text, locale) {
  if (!(props.id in configField)) {
    configField[props.id] = {}
  }
  configField[props.id][locale] = text
}

function reset(locale) {
  if (props.id in configField && locale in configField[props.id]) {
    delete configField[props.id][locale]
  }
}
</script>

<template>
  <div v-for="locale in locales">
    <span class="flex gap-2 m-1 items-center">
      <v-icon :name="'fi-' + locale" squared="false" />
      <div class="w-full h-10 items-center text-lg flex">
        &nbsp;
        <div
          :ref="idByLocale(locale)"
          contenteditable
          class="w-full h-full border rounded-sm resize-none p-1 whitespace-nowrap hover:bg-gray-100"
          @blur="setConfigText($event.target.textContent.trim(), locale)"
          @keyup.enter.exact="$event.target.blur()"
        >
          {{ initialValues[locale] }}
        </div>
      </div>
      <v-icon name="la-undo-alt-solid" @click="reset(locale)" class="cursor-pointer" />
    </span>
  </div>
</template>
