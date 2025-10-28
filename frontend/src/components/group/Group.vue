<script setup>
import { ref } from 'vue'

import Attributes from '@/components/group/Attributes.vue'
import RoleContainer from '@/components/group/RoleContainer.vue'

import {
  CheckCircleIcon,
  XCircleIcon,
  ChevronDownIcon,
  ChevronRightIcon,
} from '@heroicons/vue/24/outline'

import { useConfigStore } from '@/stores/configStore'
import { useDataStore } from '@/stores/dataStore'

const props = defineProps({
  groupId: {
    type: String,
    default: '',
  },
  expanded: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['dragged', 'dropped'])

const configStore = useConfigStore()
const dataStore = useDataStore()

const groupId = props.groupId

const expanded = ref(props.expanded)
const exclude = ref(configStore.isGroupExcluded(groupId))

const hasSubgroups =
  'subgroups' in dataStore &&
  props.groupId in dataStore.subgroups &&
  dataStore.subgroups[props.groupId].length > 0

var orderedSubgroups = hasSubgroups ? dataStore.subgroups[groupId] : null

function excludeGroup() {
  configStore.excludeGroup(groupId)
  exclude.value = true
}

function includeGroup() {
  configStore.includeGroup(groupId)
  exclude.value = false
}

// Everything regarding dragging
var draggingIndex = null
var belowDrag = ref(false)

function onDragEnter(event) {
  belowDrag.value = true
}
function onDragLeave(event) {
  belowDrag.value = false
}
function onDragged(index) {
  draggingIndex = index
}
function onDropped(index, groupId) {
  if (draggingIndex === null || draggingIndex === index) return

  const movedGroup = orderedSubgroups[draggingIndex]
  orderedSubgroups.splice(draggingIndex, 1)
  orderedSubgroups.splice(index, 0, movedGroup)
  draggingIndex = null

  configStore.groups.order[groupId] = orderedSubgroups
}
function onDrop() {
  belowDrag.value = false
  emit('dropped')
}
</script>

<template>
  <div class="flex items-center justify-between w-full text-xl rounded-lg hover:bg-gray-100">
    <span class="flex items-start w-full select-none cursor-pointer" @click="expanded = !expanded">
      <ChevronDownIcon v-if="expanded" class="mt-1.5 w-4 mr-2 cursor-pointer" />
      <ChevronRightIcon v-else class="mt-2 w-4 mr-2 cursor-pointer" />

      <span
        class="w-full"
        draggable="true"
        @dragstart="$emit('dragged')"
        @dragover.prevent=""
        @drop="onDrop()"
        @dragenter="onDragEnter"
        @dragleave="onDragLeave"
      >
        <p :class="{ 'line-through': exclude }">{{ dataStore.groups[props.groupId].name.de }}</p>
      </span>
    </span>

    <!-- Icon -->
    <div class="ml-3 cursor-pointer text-green-500" v-if="!exclude" @click="excludeGroup()">
      <CheckCircleIcon class="h-5 w-5 transition duration-300 hover:bg-teal-300/50" />
    </div>
    <div class="ml-3 cursor-pointer text-red-500" v-else @click="includeGroup()">
      <XCircleIcon class="h-5 w-5 transition duration-300 hover:bg-amber-300/50" />
    </div>
  </div>

  <!-- Subgroups -->
  <div v-show="expanded" v-if="hasSubgroups" class="p-2 m-1 mb-3 pr-1 border rounded-lg">
    <Attributes :groupId="props.groupId" />
    <!---------------->
    <hr class="mb-2 mt-2" />
    <!---------------->
    <p class="font-bold">Groups</p>

    <div v-for="(id, index) in orderedSubgroups" :key="id">
      <Group :groupId="id" @dragged="onDragged(index)" @dropped="onDropped(index, groupId)" />
    </div>
  </div>
  <!-- Group Detail -->
  <div v-else v-show="expanded" class="block p-2 m-1 border rounded-lg">
    <Attributes :groupId="props.groupId" />

    <!---------------->
    <hr class="mb-2 mt-1" />
    <!---------------->

    <p class="font-bold">Roles</p>
    <RoleContainer :groupId="groupId" />
  </div>
</template>
