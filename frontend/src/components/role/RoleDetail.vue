<script setup>
import { useConfigStore } from '@/stores/configStore'

import ConfigTextInput from '@/components/widgets/ConfigTextInput.vue'

const props = defineProps({
  roleId: {
    type: String,
  },
  role: {
    type: Object,
    default: { de: '', fr: '', it: '' },
  },
})

const configStore = useConfigStore()
</script>

<template>
  <div
    class="w-full flex p-1 text-xl justify-between select-none bg-gray-50 rounded-md hover:bg-gray-100"
  >
    <img src="/favicon.png" class="max-h-27 border rounded-lg aspect-square mr-2" />
    <div class="w-full">
      <ConfigTextInput
        :id="props.roleId"
        :configField="configStore.roles.name"
        :defaultTextDe="props.role.de"
        :defaultTextFr="props.role.fr"
        :defaultTextIt="props.role.it"
      />
    </div>
  </div>
</template>
