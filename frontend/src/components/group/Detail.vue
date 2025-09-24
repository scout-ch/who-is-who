<script setup>
import { ref } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'

import Role from '@/components/role/Role.vue'
import ExpandableRow from '@/components/widgets/ExpandableRow.vue'
import ConfigTextInput from '@/components/widgets/ConfigTextInput.vue'

const props = defineProps({
  groupId: {
    type: String,
    default: '',
  },
})

const dataStore = useDataStore()
const configStore = useConfigStore()

const expanded = ref(false)

var orderedRoles = dataStore.rolesByGroups[props.groupId]

var draggingIndex = null

function onDragged(index) {
  draggingIndex = index
}
function onDropped(index, groupId) {
  if (draggingIndex === null || draggingIndex === index) return

  const movedRole = orderedRoles[draggingIndex]
  orderedRoles.splice(draggingIndex, 1)
  orderedRoles.splice(index, 0, movedRole)
  draggingIndex = null

  configStore.roles.order[props.groupId] = orderedRoles
}
</script>

<template>
  <!-- Group attributes -->
  <ExpandableRow title="Name">
    <ConfigTextInput
      :id="props.groupId"
      :configField="configStore.groups.name"
      :defaultTextDe="dataStore.groups[props.groupId].name.de"
      :defaultTextFr="dataStore.groups[props.groupId].name.de"
      :defaultTextIt="dataStore.groups[props.groupId].name.de"
    />
  </ExpandableRow>
  <ExpandableRow title="Description">
    <ConfigTextInput :id="props.groupId" :configField="configStore.groups.description" />
  </ExpandableRow>

  <!---------------->
  <hr class="mb-2 mt-1" />
  <!---------------->

  <!-- Roles -->
  <div class="ml-2" v-for="(roleId, index) in dataStore.rolesByGroups[props.groupId]" :key="roleId">
    <Role :roleId="roleId" @dragged="onDragged(index)" @dropped="onDropped(index)" />
  </div>
</template>
