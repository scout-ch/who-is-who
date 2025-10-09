<script setup>
import { useConfigStore } from '@/stores/configStore'

import ConfigTextInput from '@/components/widgets/ConfigTextInput.vue'
import ConfigInput from '@/components/widgets/ConfigInput.vue'
import PersonImage from '@/components/widgets/PersonImage.vue'

const props = defineProps({
  roleId: {
    type: String,
  },
  person_id: {
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
  <div>
    <div class="w-full flex p-1 text-xl justify-between select-none rounded-md">
      <PersonImage :person_id="props.person_id" />
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
    <ConfigInput
      :id="props.roleId"
      :configField="configStore.roles.tel"
      label="Telefon"
      placeholder="+41 345 534 22"
    />
    <ConfigInput
      :id="props.roleId"
      :configField="configStore.roles.email"
      label="Email"
      placeholder="mail@something.ch"
    />
  </div>
</template>
