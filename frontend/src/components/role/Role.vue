<script setup>
import { ref, computed } from 'vue'
import { CheckCircleIcon, XCircleIcon, ReceiptRefundIcon } from '@heroicons/vue/24/outline'
import { useDataStore } from '@/stores/dataStore'
import { useConfigStore } from '@/stores/configStore'
import RoleDetail from './RoleDetail.vue'

const props = defineProps({
  roleId: {
    type: String,
  },
  include: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['dragged', 'dropped'])

const dataStore = useDataStore()
const configStore = useConfigStore()

// Spreading both value stores causes the second object values to overwrite the first
const role = computed(() => loadRole())
const person = dataStore.roles[props.roleId].person

const include = ref(true)

const showDetail = ref(false)

function loadRole() {
  return { ...dataStore.roles[props.roleId].name, ...configStore.roles.name[props.roleId] }
}

function excludeRole() {
  configStore.excludeRole(props.roleId)
  include.value = false
}

function includeRole() {
  configStore.includeRole(props.roleId)
  include.value = true
}

// Dragstuff
var belowDrag = ref(false)

function onDragEnter(event) {
  belowDrag.value = true
}

function onDragLeave(event) {
  belowDrag.value = false
}
function onDrop() {
  belowDrag.value = false
  emit('dropped')
}
</script>

<template>
  <div>
    <span
      class="flex items-center justify-between w-full text-xl cursor-pointer hover:bg-gray-100 rounded-lg"
    >
      <div
        class="flex w-full justify-between mr-7 select-none"
        draggable="true"
        @click="showDetail = !showDetail"
        @dragover.prevent=""
        @dragstart="$emit('dragged')"
        @drop="onDrop()"
        @dragenter="onDragEnter"
        @dragleave="onDragLeave"
      >
        <!-- Role Values -->
        <span>
          <p :class="{ 'line-through': !include }">
            {{ person.firstname }} {{ person.lastname }} / {{ person.nickname }}
          </p>
        </span>
        <span class="flex gap-3">
          <p v-for="locale in ['de', 'fr', 'it']">{{ role[locale] }}</p>
        </span>
      </div>
      <div class="flex items-center">
        <!-- Icons -->
        <div class="w-5 mr-2" />
        <div class="cursor-pointer text-green-500" v-if="include" @click="excludeRole">
          <CheckCircleIcon class="h-5 w-5 transition duration-300 hover:bg-teal-300/50" />
        </div>
        <div class="cursor-pointer text-red-500" v-else="include" @click="includeRole">
          <XCircleIcon class="h-5 w-5 transition duration-300 hover:bg-amber-300/50" />
        </div>
      </div>
    </span>
    <RoleDetail v-show="showDetail" :roleId="props.roleId" :personId="person.id" :role="role" />
  </div>
</template>
