<script setup>
import { useTemplateRef, computed } from 'vue'

const locales = ['de', 'fr', 'it']

const props = defineProps({
  id: {
    type: String,
  },
  configField: {
    type: Object,
  },
  defaultValues: {
    type: Object,
    default: {},
  },
})
const initialValues = computed(() => {
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
  if (!(props.id in props.configField)) {
    props.configField[props.id] = {}
  }
  props.configField[props.id][locale] = text
}

function reset(locale) {
  if (props.id in props.configField && locale in props.configField[props.id]) {
    delete props.configField[props.id][locale]
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
