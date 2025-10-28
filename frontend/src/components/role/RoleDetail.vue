<script setup>
import { useConfigStore } from '@/stores/configStore'
import { useDataStore } from '@/stores/dataStore'

import ConfigTextInput from '@/components/widgets/ConfigTextInput.vue'
import ConfigInput from '@/components/widgets/ConfigInput.vue'
import PersonImage from '@/components/widgets/PersonImage.vue'

const props = defineProps({
  roleId: {
    type: String,
  },
  personId: {
    type: String,
  },
  role: {
    type: Object,
  },
})

const dataStore = useDataStore()
const configStore = useConfigStore()
</script>

<template>
  <div>
    <div class="w-full flex p-1 text-xl justify-between select-none rounded-md">
      <PersonImage :person_id="props.personId" />
      <div class="w-full">
        <ConfigTextInput
          :id="props.roleId"
          :configField="configStore.roles.name"
          :defaultValues="props.role"
        />
      </div>
    </div>
    <ConfigInput :id="props.roleId" :configField="configStore.roles.tel" label="Telefon" />
    <ConfigInput :id="props.roleId" :configField="configStore.roles.email" label="Email" />
  </div>
</template>
