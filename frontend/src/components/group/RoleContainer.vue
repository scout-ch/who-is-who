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
  <div class="ml-2" v-for="(roleId, index) in dataStore.rolesByGroups[props.groupId]" :key="roleId">
    <Role :roleId="roleId" @dragged="onDragged(index)" @dropped="onDropped(index)" />
  </div>
</template>
