<script setup>
import { useTemplateRef } from 'vue'

const locales = ['de', 'fr', 'it']

const props = defineProps({
  id: {
    type: String,
  },
  configField: {
    type: Object,
  },
  defaultTextDe: {
    type: String,
    default: '',
  },
  defaultTextFr: {
    type: String,
    default: '',
  },
  defaultTextIt: {
    type: String,
    default: '',
  },
})
const defaultText = { de: props.defaultTextDe, fr: props.defaultTextFr, it: props.defaultTextIt }

const ctinput = {
  de: useTemplateRef('ctinputde'),
  fr: useTemplateRef('ctinputfr'),
  it: useTemplateRef('ctinputit'),
}

function setText(text, locale) {
  if (!(props.id in props.configField)) {
    props.configField[props.id] = {}
  }
  props.configField[props.id][locale] = text
}

function reset(locale) {
  if (!(props.id in props.configField)) {
    return
  }
  if (locale) {
    ctinput[locale].value[0].textContent = defaultText[locale]
    props.configField[props.id][locale] = defaultText[locale]

    // TODO: small optimisation: check if all entries in the configField are equal to the default text and remove the entry for the id if so
  } //else {
  //delete props.configField[props.id]
  //locales.forEach((loc) => {

  //})
  //}
}
</script>

<template>
  <div v-for="locale in locales">
    <span class="flex gap-2 m-1 items-center">
      <v-icon :name="'fi-' + locale" squared="false" />
      <div
        :ref="'ctinput' + locale"
        contenteditable="true"
        class="w-full border rounded-sm resize-none h-10 p-1 items-center text-lg flex hover:bg-gray-100"
        @keyup="setText($event.target.textContent, locale)"
        @keyup.enter.exact="$event.target.blur()"
        :textContent="defaultText[locale]"
      />
      <v-icon name="la-undo-alt-solid" @click="reset(locale)" class="cursor-pointer" />
    </span>
  </div>
</template>
