<script setup>
import { ref } from 'vue'
import Group from './Group.vue'
import axios from 'axios'

import { useDataStore } from '@/stores/dataStore'

const dataStore = useDataStore()

const root_group = '2'

const loading = ref(true)

axios
  .get('/api')
  .then((response) => {
    const data = response['data']
    dataStore.groups = data['groups']
    dataStore.subgroups = data['subgroups_for_groups']
    dataStore.roles = data['roles']
    dataStore.rolesByGroups = data['roles_for_groups']
    loading.value = false
  })
  .catch((error) => {
    console.error(error)
  })
</script>

<template>
  <div v-if="loading"><p>Loading...</p></div>
  <div v-else>
    <Group :groupId="root_group" :expanded="true" />
  </div>
</template>
