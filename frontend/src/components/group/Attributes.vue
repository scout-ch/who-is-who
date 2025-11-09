<script setup>
import ConfigTextInput from '@/components/widgets/ConfigTextInput.vue'
import ExpandableRow from '@/components/widgets/ExpandableRow.vue'

import { useDataStore } from '@/stores/dataStore'

const props = defineProps({
  groupId: {
    type: String,
    default: '',
  },
})

const dataStore = useDataStore()
</script>

<template>
  <!-- Group attributes -->
  <p class="font-bold">Attributes</p>
  <ExpandableRow title="Name">
    <ConfigTextInput
      :id="props.groupId"
      configFieldName="groups.name"
      :defaultValues="{ ...dataStore.groups[props.groupId].name }"
    />
  </ExpandableRow>
  <ExpandableRow title="Description">
    <ConfigTextInput :id="props.groupId" configFieldName="groups.description" />
  </ExpandableRow>
</template>
