<script setup>
import { ref } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'

import Role from '@/components/role/Role.vue'

const props = defineProps({
  groupId: {
    type: String,
    default: '',
  },
})

const dataStore = useDataStore()
const configStore = useConfigStore()

const orderedRoles = ref([])

// Load role ids if roles in groups
if (props.groupId in dataStore.rolesByGroups) {
  orderedRoles.value = [...dataStore.rolesByGroups[props.groupId]]

  // Overwrite with order config if present
  if (props.groupId in configStore.roles.order) {
    orderedRoles.value = [...configStore.roles.order[props.groupId]]
  }
}

var draggingIndex = null

function onDragged(index) {
  draggingIndex = index
}
function onDropped(index) {
  if (draggingIndex === null || draggingIndex === index) return

  const movedRole = orderedRoles.value[draggingIndex]
  orderedRoles.value.splice(draggingIndex, 1)
  orderedRoles.value.splice(index, 0, movedRole)
  draggingIndex = null

  configStore.roles.order[props.groupId] = orderedRoles
}
</script>
<template>
  <!-- Roles -->
  <div class="ml-2" v-for="(roleId, index) in orderedRoles" :key="roleId">
    <Role :roleId="roleId" @dragged="onDragged(index)" @dropped="onDropped(index)" />
  </div>
</template>
